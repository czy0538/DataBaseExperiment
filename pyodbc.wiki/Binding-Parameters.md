
## Performance

One complication with binding parameters
using [SQLBindParameter](https://msdn.microsoft.com/en-us/library/ms710963.aspx) is we need to
tell it information that pyodbc cannot deduce from the values being passed.  We have to provide
not only the source C data type, which is easy, but also the SQL type such as VARCHAR(10).
There is no way for pyodbc to know whether the value "test" should be a CHAR(4), WCHAR(4) or
VARCHAR(20).  Unfortunately there isn't an easy solution to this.

We can get pretty far by making "close enough" guesses.  If we have an `int` we can send it as
an INTEGER or BIGINT based on its size.  Strings could be sent as VARCHAR with the size set to
the length of the variable.  Unfortunately this doesn't solve everything:

* If we pass VARCHAR to an Oracle comparison with a CHAR field, they won't match.
* SQL Server will create and cache a new query plan for *every* different parameter length we provide.
* `None` could be a NULL of any type.  VARCHAR can be converted to most types, but SQL Server
  won't convert it to binary, so we get an error inserting into binary columns.

We can prepare the SQL which cause the server to analyze it and we can then ask it what it
thinks of the parameters, but this has two important issues:

1. The most important is that it is expensive.  It requires the SQL to be sent across the
   network, the server to process it, and then the results sent back across the network.
2. Sometimes the type cannot be determined from the SQL.  Given "select ? as id", the server
   cannot determine a type and will give us an error when we ask about the type.

### Issues In Detail

#### SQLDescribeParam may not be supported

It is important to note that SQLDescribeParam is not supported by a lot of drivers.  This is
checked and stored in the "connection info" and made available at
`cnxn->supports_describeparam`.

#### SQL Server Cached Query Plans

SQL Server creates and caches a new query plan for the same prepared SQL if the parameter
lengths differ.  For example, the following will create two query plans:

```python
c.execute("insert into t1 values (?)", "x")
c.execute("insert into t1 values (?)", "yy")
```

Personally I consider this is a bug - these can't create drastically different access plans but
the almost-duplicate query plans do end up taking a very large amount of memory better served
for real work.

#### Writing NULL

SQL Server checks for data type compatibility even for NULL and fails if the value and
parameter types are not compatible.  Personally I think this is something they should handle to
better work with dynamic languages where variables don't have intrinsic types.

Unfortunately there isn't a SQL Server type that can be converted to every other type.  The
closest is varchar which can be converted to everything except binary.

```text
[42000] [Microsoft][SQL Server Native Client 11.0][SQL Server]
Implicit conversion from data type varchar to varbinary is not allowed. Use the CONVERT
function to run this query.
```

Versions 3 and 4 of pyodbc always prepare the statement and call SQLDescribeParam only when
`None` is passed.

#### Oracle CHAR vs VARCHAR

It has been reported that Oracle will not match a varchar against an equivalent string in a
char column if the parameter is not space padded.

```python
val = 'test'
c.execute("create table t1(s char(10))")
c.execute("insert into t1 values (?)")
c.execute("select count(*) from t1 where s=?", val) # returns zero
```

According to the [Oracle documentation](https://docs.oracle.com/cd/B10501_01/appdev.920/a96624/b_char.htm),
if either value in a comparison is a varchar, blanks are not removed for the comparison
("non-blank-padding semantics are used").

This occurs because pyodbc doesn't know how the string is being used, just that it is a string
and its length.  Therefore it passes it as a varchar with length exactly matching the value.

I've confirmed that PostgreSQL, MySQL, and SQL Server do not do this.

I'm not sure that the behavior is "wrong".  While I would find it annoying, I wouldn't
use a CHAR column for variable length data.  (There are some reasons like extreme
optimizations, but I'm not sure how valid those remain.)  It might be correct behavior (for
Oracle, at least) that can be worked around with casting:

```sql
select count(*)
  from t1
 where s = (cast ? as char(10))
```

#### Informix VARCHAR vs LONGVARCHAR

According to issue #260, Informix requires varchar fields to be sent as type SQL_VARCHAR but
text fields to be sent as SQL_LONGVARCHAR.

As of version 4.0.17, the code uses SQLGetTypeInfo to determine the maximum sizes for varchar
and uses SQL_LONGVARCHAR for anything longer than that.

### Solutions and Workarounds

The only solution I know of for the NULL and CHAR issues are to prepare an examine the
parameters.  If the database cannot tell us the type, use VARCHAR and length 1 for `None` and
the data length of strings.

The query plan issue could be mitigated by rounding variable length sizes to large multiples
like 1K, 4K, 20K, etc.  This would still allow multiple query plans to be cached, but would be
much fewer.  We might even consider hardcoding the maximum, but I wonder if that
would change the access plan?  (It seems like the plan should not depend on the length, but if
it didn't why do we have multiple when length differs by 1 character?)

Since PostgreSQL and MySQL are very common and don't require any of these, it is probably worth
making a way to disable preparation for performance.  In that case, statements would only be
prepared if used more than once.

Since there is no way to reduce prepares for Oracle, it might be worth allowing the types to be
cached.  We already cache the types for the latest prepare but it could be extended to allow us
to keep the last few statements.

#### Proposal 1

This is a really messy, stream-of-consciousness API, but consider it a brainstorming session to
be improved upon.

If we put all of these together, it might look like this:

By default pyodbc always prepares SQL with parameters and calls SQLDescribeParam on each
parameter.  The results are used to provide precise values for the parameters.

The preparation cache size starts at zero, meaning it is disabled.  It can be turned on by
setting its size to a non-zero value.  All SQL statements with parameters that are not found in
the cache are prepared and added to the cache.

    pyodbc.set_prepare_cache_size(50)

To not prepare always, set the handling of variable length binding:

    # This is the default which causes all SQL with params to be prepared
    pyodbc.set_var_binding_length(None)

    # Using a positive integer causes the values to be rounded up.  This would be used on SQL
    # Server to round values to nearest 4K:
    pyodbc.set_var_binding_length(4096)

    # To set the parameter length to the length of the data with no rounding, set the value to 1.
    pyodbc.set_var_binding_length(1)

With the above set, SQL statements will still be prepared if there is a NULL parameter.  To
disable this and always send `None` as varchar(1) use:

    pyodbc.set_none_binding(pyodbc.SQL_VARCHAR)

If the variable binding length and NULL value binding are both set, statements will not be
prepared unless they are used twice in a row.

To summarize by database:

For Oracle, do not set anything.  This is the slowest but is required.

For SQL Server, we need to prepare for None but not for character types.  Set the variable
binding length to something large to reduce the number of query plans:

    pyodbc.set_var_binding_length(4096)

For PostgreSQL and MySQL, preparing is never needed except for performance so send exact
lengths and send None as varchar:

    pyodbc.set_var_binding_length(1)
    pyodbc.set_none_binding(pyodbc.SQL_VARCHAR)

#### Proposal 2

Perhaps it would make sense to always take the "slow" approach and use SQLDescribeParam (when
available), but optimize it by caching the information by SQL statement.

An MRU cache could be used and shared among connections by associating it with the `CnxnInfo`
object.  One of these is created for each connection string (but hashed to not expose the
password).  If the cache is part of the connection info, each new connection with the same
connection string could share it.

I (Kleehammer) really thought I did this at one point and liked the results.

To help with issues like #260 where the same Python type (`str`) needs to be sent with two different SQL types (`SQL_VARCHAR` or `SQL_LONGVARCHAR`) based on the database's type, we could also allow conversion functions to be installed that would be passed both the Python type and the parameter type obtained from SQLDescribeParam and would be responsible for setting (or just overriding) the SQL type used to send.
