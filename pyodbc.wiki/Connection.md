Once a connection to the database has been established using the pyodbc [connect()](The-pyodbc-Module#connect) function, connection objects are used to manage operations on that connection. Each connection object manages a single ODBC connection (specifically a single HDBC). Connections also manage database transactions.

For reference, the Python DB API for connections is [here](https://www.python.org/dev/peps/pep-0249/#connection-objects).

## Connection Attributes

### autocommit
Setting `autocommit` True will cause the database to issue a commit after each SQL statement, otherwise database transactions will have to be explicity committed. As per the [Python DB API](https://www.python.org/dev/peps/pep-0249/), the default value is False (even though the ODBC default value is [True](https://msdn.microsoft.com/en-us/library/ms131281.aspx)).  Typically, you will probably want to set `autocommit` True when creating a connection.

This value can be changed on a connection dynamically (e.g. `cnxn.autocommit = True`), and all subsequent SQL statements will be executed using the new setting.

Auto-commit typically needs to be `True` for DDL operations that cannot be rolled-back, e.g. dropping a database.

### searchescape
The ODBC search pattern escape character, as returned by [SQLGetInfo](https://msdn.microsoft.com/en-us/library/ms711681%28v=vs.85%29.aspx)(SQL\_SEARCH\_PATTERN\_ESCAPE), used to escape special characters such as '%' and ''. These are driver specific.

### timeout
The timeout value, in seconds, for SQL queries (note, not database connections). Use zero, the default, to disable.

The timeout is applied to all cursors created by the connection, so it cannot be changed for a specific cursor or SQL statement. If a query timeout occurs, the database should raise an OperationalError exception with SQLSTATE HYT00 or HYT01.

Note, this attribute affects only SQL queries. To set the timeout when making a database connection, use the `timeout` parameter with the pyodbc [connect()](The-pyodbc-Module#connect) function.

## Connection Functions

### cursor()

Returns a new Cursor object using the connection.

`mycursor = cnxn.cursor()`

pyodbc supports multiple cursors per connection but your database may not.

### commit()
Commits all SQL statements executed on the connection since the last commit/rollback.

`cnxn.commit()`

Note, this will commit the SQL statements from ALL the cursors created from this connection.

### rollback()
Rolls back all SQL statements executed on the connection since the last commit.

`cnxn.rollback()`

You can call this even if no SQL statements have been executed on the connection, allowing it to be used in `finally` statements, etc.

### close()
Closes the connection.  Note, any uncommitted effects of SQL statements on the database from this connection will be rolled back and lost forever!

`cnxn.close()`

Connections are automatically closed when they are deleted (typically when they go out of scope) so you should not normally need to call this, but you can explicitly close the connection if you wish.

Trying to use a connection after it has been closed will result in a ProgrammingError exception.

### getinfo()
This function is not part of the Python DB API.

Returns general information about the driver and data source associated with a connection by calling [SQLGetInfo](https://msdn.microsoft.com/en-us/library/ms711681.aspx), e.g.:

`data_source_name = cnxn.getinfo(pyodbc.SQL_DATA_SOURCE_NAME)`

See Microsoft's SQLGetInfo [documentation](https://msdn.microsoft.com/en-us/library/ms711681.aspx "SQLGetInfo function") for the types of information available.

### execute()
This function is not part of the Python DB API.

Creates a new Cursor object, calls its execute method, and returns the new cursor.

`num_products = cnxn.execute("SELECT COUNT(*) FROM product")`

See Cursor.execute() for more details. This is a convenience method that is not part of the DB API. Since a new Cursor is allocated by each call, this should not be used if more than one SQL statement needs to be executed on the connection.

### add_output_converter()

Register an output converter function that will be called whenever a value with the given SQL type is read from the database.

```python
add_output_converter(sqltype, func)
```

* `sqltype`: the integer SQL type value to convert, which can be one of the defined standard constants (e.g. `pyodbc.SQL_VARCHAR`) or a database-specific value (e.g. `-151` for the SQL Server 2008 geometry data type).
* `func`: the converter function which will be called with a single parameter, the value, and should return the converted value. If the value is NULL then the parameter passed to the function will be `None`, otherwise it will be a `<class 'bytes'>` object.

For an example, see [Using an Output Converter function](Using-an-Output-Converter-function).

### clear_output_converters()

Removes all output converter functions.

### remove_output_converter()

Remove a single output converter function previously registered with `add_output_converter`. *(New in version 4.0.25.)*

```python
remove_output_converter(sqltype)
```

### get_output_converter()

Return a reference to the currently active output converter function previously registered with `add_output_converter`. *(New in version 4.0.26.)*

```python
prev_converter = get_output_converter(sqltype)
add_output_converter(sqltype, new_converter)
#
# do stuff that requires the new converter ...
#
add_output_converter(sqltype, prev_converter)  # restore previous behaviour
```

### setencoding()

    # Python 2
    cnxn.setencoding(type, encoding=None, ctype=None)

    # Python 3
    cnxn.setencoding(encoding=None, ctype=None)

Sets the text encoding for SQL statements and text parameters.

##### type

The text type to configure.  In Python 2 there are two text types: `str` and `unicode` which
can be configured indivually.  Python 3 only has `str` (which is Unicode), so the parameter is
not needed.


##### encoding

The encoding to use.  This must be a valid Python encoding that converts text to `bytes`
(Python 3) or `str` (Python 2).

##### ctype

The C data type to use when passing data: `pyodbc.SQL_CHAR` or `pyodbc.SQL_WCHAR`.

If not provided, `SQL_WCHAR` is used for "utf-16", "utf-16le", and "utf-16be".  `SQL_CHAR` is
used for all other encodings.

The defaults are:

Python version | type | encoding | ctype
-------------- | ---- | -------- | -----
Python 2 | str | utf-8 | SQL_CHAR
Python 2 | unicode | utf-16le | SQL_WCHAR
Python 3 | unicode | utf-16le | SQL_WCHAR

If your database driver communicates with only UTF-8 (often MySQL and PostgreSQL), try the
following:

      # Python 2
      cnxn.setencoding(str, encoding='utf-8')
      cnxn.setencoding(unicode, encoding='utf-8')

      # Python 3
      cnxn.setencoding(encoding='utf-8')

In Python 2.7, the value "raw" can be used as special encoding for `str` objects.  This will
pass the string object's bytes as-is to the database.  This is not recommended as you need to
make sure that the internal format matches what the database expects.

### setdecoding()

      # Python 2
      cnxn.setdecoding(sqltype, encoding=None, ctype=None, to=None)

      # Python 3
      cnxn.setdecoding(sqltype, encoding=None, ctype=None)

Sets the text decoding used when reading `SQL_CHAR` and `SQL_WCHAR` from the database.

#### sqltype

The SQL type being configured: `pyodbc.SQL_CHAR` or `pyodbc.SQL_WCHAR`.

There is a special flag, `pyodbc.SQL_WMETADATA`, for configuring the decoding of column names
from SQLDescribeColW.

#### encoding

The Python encoding to use when decoding the data.

#### ctype

The C data type to request from SQLGetData: `pyodbc.SQL_CHAR` or `pyodbc.SQL_WCHAR`.

#### to

The Python 2 text data type to be returned: `str` or `unicode`.  If not provided (recommended),
whatever type the codec returns is returned.  (This parameter is not needed in Python 3 because
the only text data type is `str`.)

The defaults are:

Python version | type | encoding | ctype
-------------- | ---- | -------- | -----
Python 2 | str | utf-8 | SQL_CHAR
Python 2 | unicode | utf-16le | SQL_WCHAR
Python 2 | unicode | utf-16le | SQL_WMETADATA
Python 3 | unicode | utf-16le | SQL_WCHAR
Python 3 | unicode | utf-16le | SQL_WMETADATA

In Python 2.7, the value "raw" can be used as special encoding for `SQL_CHAR` values.  This
will create a `str` object directly from the bytes from the database with no conversion.string
object's bytes as-is to the database.  This is not recommended as you need to make sure that
the internal format matches what the database sends.

### set_attr()

      cnxn.set_attr(attr_id, value)

Sets an attribute on the connection via
[SQLSetConnectAttr](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlsetconnectattr-function)
.   The id must be an integer constant defined by ODBC or the driver.  Some common attributes
and values are listed in the pyodbc module, e.g.:

      cnxn.set_attr(pyodbc.SQL_ATTR_TXN_ISOLATION, pyodbc.SQL_TXN_REPEATABLE_READ)

At this time, only integer values are supported and are always passed as SQLUINTEGER.

## Context Manager

Connection objects do support the Python context manager syntax (the `with` statement), but it's important to understand the "context" in this scenario. For example, the following code:
```python
with pyodbc.connect('mydsn') as cnxn:
    do_stuff
```    
is essentially equivalent to:
```python
cnxn = pyodbc.connect('mydsn')
do_stuff
if not cnxn.autocommit:
    cnxn.commit()  
```
As you can see, `commit()` is called when the context is exited, even if `autocommit` is False.
Hence, the "context" here is not so much the connection itself. Rather, it's better to think of it as a database transaction that will be committed without explicitly calling `commit()`.

Note, the connection object is not closed when the context is exited.
