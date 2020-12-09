The Cursor object represents a database cursor, which is typically used to manage the context of a fetch operation. Database cursors map to ODBC HSTMTs. Cursors created from the same connection are not isolated, i.e. any changes done to the database by one cursor are immediately visible by the other cursors.  Note, cursors do not manage database transactions, transactions are committed and rolled-back from the connection.

## Cursor Attributes

### description
This read-only attribute is a list of 7-item tuples, one tuple for each column returned by the last SQL select statement.  Each tuple contains:

1. column name (or alias, if specified in the SQL)
1. type code
1. display size (pyodbc does not set this value)
1. internal size (in bytes)
1. precision
1. scale
1. nullable (True/False)

This attribute will be None for operations that do not return rows or if one of the execute methods has not been called.  The 'type code' value is the class type used to create the Python objects when reading rows. For example, a varchar column's type will be `str`.

### rowcount
The number of rows modified by the last SQL statement.

This is -1 if no SQL has been executed or if the number of rows is unknown. Note that it is not uncommon for databases to report -1 immediately after a SQL select statement for performance reasons. (The exact number may not be known before the first records are returned to the application.)

## Cursor Functions

### execute(sql, *parameters)
Prepares and executes a SQL statement, **returning the Cursor object itself.** The optional parameters may be passed as a sequence, as specified by the DB API, or as individual values.
```python
# standard
cursor.execute("select a from tbl where b=? and c=?", (x, y))
```
```python
# pyodbc extension
cursor.execute("select a from tbl where b=? and c=?", x, y)
```
The return value is always the cursor itself:
```python
for row in cursor.execute("select user_id, user_name from users"):
    print(row.user_id, row.user_name)

row  = cursor.execute("select * from tmp").fetchone()
rows = cursor.execute("select * from tmp").fetchall()

count = cursor.execute("update users set last_logon=? where user_id=?", now, user_id).rowcount
count = cursor.execute("delete from users where user_id=1").rowcount
```
As suggested in the DB API, the last prepared statement is kept and reused if you execute the same SQL again, making executing the same SQL with different parameters will be more efficient.

### executemany(sql, *params), with fast_executemany=False (the default)

Executes the same SQL statement for each set of parameters, returning None. The single `params` parameter must be a sequence of sequences, or a generator of sequences.
```python
params = [ ('A', 1), ('B', 2) ]
cursor.executemany("insert into t(name, id) values (?, ?)", params)
```
This will execute the SQL statement twice, once with ('A', 1) and once with ('B', 2).  That is, the above code is essentially equivalent to:
```python
params = [ ('A', 1), ('B', 2) ]
for p in params:
    cursor.execute("insert into t(name, id) values (?, ?)", p)
```
Hence, running executemany() with fast_executemany=False is generally not going to be much faster than running multiple execute() commands directly.

Note, after running executemany(), the number of affected rows is NOT available in the `rowcount` attribute.

Also, be careful if `autocommit` is True.  In this scenario, the provided SQL statement will be committed for each and every record in the parameter sequence.  So if an error occurs part-way through processing, you will end up with some of the records committed in the database and the rest not, and it may be not be easy to tell which records have been committed.  Hence, you may want to consider setting `autocommit` to False (and explicitly `commit()` / `rollback()`) to make sure either all the records are committed to the database or none are, e.g.:
```python
try:
    cnxn.autocommit = False
    params = [ ('A', 1), ('B', 2) ]
    cursor.executemany("insert into t(name, id) values (?, ?)", params)
except pyodbc.DatabaseError as err:
    cnxn.rollback()
else:
    cnxn.commit()
finally:
    cnxn.autocommit = True
```

### executemany(sql, *params), with fast_executemany=True

Executes the SQL statement for the entire set of parameters, returning None. The single `params` parameter must be a sequence of sequences, or a generator of sequences.
```python
params = [ ('A', 1), ('B', 2) ]
cursor.fast_executemany = True
cursor.executemany("insert into t(name, id) values (?, ?)", params)
```
Here, all the parameters are sent to the database server in one bundle (along with the SQL statement), and the database executes the SQL against all the parameters as one database transaction.  Hence, this form of executemany() should be much faster than the default executemany().  However, there are limitations to it, see [`fast_executemany`](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fast_executemany) for more details.

Note, after running executemany(), the number of affected rows is NOT available in the `rowcount` attribute.

Under the hood, there is one important difference when fast_executemany=True.  In that case, on the client side, pyodbc converts the Python parameter values to their ODBC "C" equivalents, based on the target column types in the database.  E.g., a string-based date parameter value of "2018-07-04" is converted to a C date type binary value by pyodbc before sending it to the database.  When fast_executemany=False, that date string is sent as-is to the database and the database does the conversion.  This can lead to some subtle differences in behavior depending on whether fast_executemany is True or False.

### fetchone()
Returns the next row in the query, or None when no more data is available.

A ProgrammingError exception is raised if no SQL has been executed or if it did not return a result set (e.g. was not a SELECT statement).
```python
cursor.execute("select user_name from users where user_id=?", userid)
row = cursor.fetchone()
if row:
    print(row.user_name)
```

### fetchval()
Returns the first column of the first row if there are results.
For more info see [Features beyond the DB API](https://github.com/mkleehammer/pyodbc/wiki/Features-beyond-the-DB-API#fetchval)

### fetchall()
Returns a list of all the remaining rows in the query.

Since this reads all rows into memory, it should not be used if there are a lot of rows. Consider iterating over the rows instead. However, it is useful for freeing up a Cursor so you can perform a second query before processing the resulting rows.

A ProgrammingError exception is raised if no SQL has been executed or if it did not return a result set (e.g. was not a SELECT statement).
```python
cursor.execute("select user_id, user_name from users where user_id < 100")
rows = cursor.fetchall()
for row in rows:
    print(row.user_id, row.user_name)
```

### fetchmany(size=cursor.arraysize)
Returns a list of remaining rows, containing no more than `size` rows, used to process results in chunks. The list will be empty when there are no more rows.

The default for cursor.arraysize is 1 which is no different than calling fetchone().

A ProgrammingError exception is raised if no SQL has been executed or if it did not return a result set (e.g. was not a SELECT statement).

### commit()
Commits all SQL statements executed on the connection that created this cursor, since the last commit/rollback.

This affects all cursors created by the same connection!

This is no different than calling commit on the connection. The benefit is that many uses can now just use the cursor and not have to track the connection.

### rollback()
Rolls back all SQL statements executed on the connection that created this cursor, since the last commit/rollback.

This affects all cursors created by the same connection!

### skip(count)
Skips the next `count` records in the query by calling [SQLFetchScroll](https://msdn.microsoft.com/en-us/library/ms714682%28v=vs.85%29.aspx) with SQL_FETCH_NEXT.

For convenience, skip(0) is accepted and will do nothing.

### nextset()
This method will make the cursor skip to the next available result set, discarding any remaining rows from the current result set. If there are no more result sets, the method returns False. Otherwise, it returns a True and subsequent calls to the fetch methods will return rows from the next result set.

This method is primarily used if you have stored procedures that return multiple results.

### close()
Closes the cursor. A ProgrammingError exception will be raised if any operation is attempted with the cursor.

Cursors are closed automatically when they are deleted (typically when they go out of scope), so calling this is not usually necessary.

### setinputsizes(list_of_value_tuples)

This optional method can be used to explicitly declare the types and sizes of query parameters. For example:

```python
sql = "INSERT INTO product (item, price) VALUES (?, ?)"
params = [('bicycle', 499.99), ('ham', 17.95)]
# specify that parameters are for NVARCHAR(50) and DECIMAL(18,4) columns
crsr.setinputsizes([(pyodbc.SQL_WVARCHAR, 50, 0), (pyodbc.SQL_DECIMAL, 18, 4)])
#
crsr.executemany(sql, params)
```

### setoutputsize()
This is optional in the API and is not supported.

### callproc(procname [,parameters])
This is not yet supported since there is no way for pyodbc to determine which parameters are input, output, or both.

You will need to call stored procedures using execute(). You can use your database's format or the ODBC escape format. For more information, see the [Calling Stored Procedures](https://github.com/mkleehammer/pyodbc/wiki/Calling-Stored-Procedures) page.

### tables(table=None, catalog=None, schema=None, tableType=None)
Returns an iterator for generating information about the tables in the database that match the given criteria.

The table, catalog, and schema interpret the '_' and '%' characters as wildcards. The escape character is driver specific, so use Connection.searchescape.

Each row has the following columns. See the [SQLTables](https://msdn.microsoft.com/en-us/library/ms711831.aspx) documentation for more information.

1. table_cat: The catalog name.
1. table_schem: The schema name.
1. table_name: The table name.
1. table_type: One of the string values 'TABLE', 'VIEW', 'SYSTEM TABLE', 'GLOBAL TEMPORARY', 'LOCAL TEMPORARY', 'ALIAS', 'SYNONYM', or a datasource specific type name.
1. remarks: A description of the table.
```python
for row in cursor.tables():
    print(row.table_name)

# Does table 'x' exist?
if cursor.tables(table='x').fetchone():
   print('yes it does')
```
### columns(table=None, catalog=None, schema=None, column=None)
Creates a result set of column information in the specified tables using the [SQLColumns](https://msdn.microsoft.com/en-us/library/ms711683(VS.85).aspx) function.

Each row has the following columns:

1. table_cat
1. table_schem
1. table_name
1. column_name
1. data_type
1. type_name
1. column_size
1. buffer_length
1. decimal_digits
1. num_prec_radix
1. nullable
1. remarks
1. column_def
1. sql_data_type
1. sql_datetime_sub
1. char_octet_length
1. ordinal_position
1. is_nullable: One of SQL_NULLABLE, SQL_NO_NULLS, SQL_NULLS_UNKNOWN.
```python
# columns in table x
for row in cursor.columns(table='x'):
    print(row.column_name)
```

### statistics(table, catalog=None, schema=None, unique=False, quick=True)
Creates a result set of statistics about a single table and the indexes associated with the table by executing [SQLStatistics](https://msdn.microsoft.com/en-us/library/ms711022(VS.85).aspx).

If `unique` is True only unique indexes are returned; if False all indexes are returned.

If `quick` is True, CARDINALITY and PAGES are returned only if they are readily available. Otherwise NULL is returned on those columns.

Each row has the following columns:

1. table_cat
1. table_schem
1. table_name
1. non_unique
1. index_qualifier
1. index_name
1. type
1. ordinal_position
1. column_name
1. asc_or_desc
1. cardinality
1. pages
1. filter_condition

### rowIdColumns(table, catalog=None, schema=None, nullable=True)
Executes [SQLSpecialColumns](https://msdn.microsoft.com/en-us/library/ms714602(VS.85).aspx) with SQL_BEST_ROWID which creates a result set of columns that uniquely identify a row.

Each row has the following columns.

1. scope: One of SQL_SCOPE_CURROW, SQL_SCOPE_TRANSACTION, or SQL_SCOPE_SESSION
1. column_name
1. data_type: The ODBC SQL data type constant (e.g. SQL_CHAR)
1. type_name
1. column_size
1. buffer_length
1. decimal_digits
1. pseudo_column: One of SQL_PC_UNKNOWN, SQL_PC_NOT_PSEUDO, SQL_PC_PSEUDO

### rowVerColumns(table, catalog=None, schema=None, nullable=True)
Executes [SQLSpecialColumns](https://msdn.microsoft.com/en-us/library/ms714602(VS.85).aspx) with SQL_ROWVER which creates a result set of columns that are automatically updated when any value in the row is updated. Returns the Cursor object. Each row has the following columns.

1. scope: One of SQL_SCOPE_CURROW, SQL_SCOPE_TRANSACTION, or SQL_SCOPE_SESSION
1. column_name
1. data_type: The ODBC SQL data type constant (e.g. SQL_CHAR)
1. type_name
1. column_size
1. buffer_length
1. decimal_digits
1. pseudo_column: One of SQL_PC_UNKNOWN, SQL_PC_NOT_PSEUDO, SQL_PC_PSEUDO

### primaryKeys(table, catalog=None, schema=None)
Creates a result set of column names that make up the primary key for a table by executing the [SQLPrimaryKeys](http://msdn.microsoft.com/en-us/library/ms711005%28VS.85%29.aspx) function.

Each row has the following columns:

1. table_cat
1. table_schem
1. table_name
1. column_name
1. key_seq
1. pk_name

### foreignKeys(table=None, catalog=None, schema=None, foreignTable=None, foreignCatalog=None, foreignSchema=None)
Executes the [SQLForeignKeys](http://msdn.microsoft.com/en-us/library/ms709315%28VS.85%29.aspx) function and creates a result set of column names that are foreign keys in the specified table (columns in the specified table that refer to primary keys in other tables) or foreign keys in other tables that refer to the primary key in the specified table.

Each row has the following columns:

1. pktable_cat
1. pktable_schem
1. pktable_name
1. pkcolumn_name
1. fktable_cat
1. fktable_schem
1. fktable_name
1. fkcolumn_name
1. key_seq
1. update_rule
1. delete_rule
1. fk_name
1. pk_name
1. deferrability

### procedures(procedure=None, catalog=None, schema=None)
Executes [SQLProcedures](http://msdn.microsoft.com/en-us/library/ms715368%28VS.85%29.aspx) and creates a result set of information about the procedures in the data source. Each row has the following columns:

1. procedure_cat
1. procedure_schem
1. procedure_name
1. num_input_params
1. num_output_params
1. num_result_sets
1. remarks
1. procedure_type

### getTypeInfo(sqlType=None)
Executes [SQLGetTypeInfo](http://msdn.microsoft.com/en-us/library/ms714632%28VS.85%29.aspx) a creates a result set with information about the specified data type or all data types supported by the ODBC driver if not specified. Each row has the following columns:

1. type_name
1. data_type
1. column_size
1. literal_prefix
1. literal_suffix
1. create_params
1. nullable
1. case_sensitive
1. searchable
1. unsigned_attribute
1. fixed_prec_scale
1. auto_unique_value
1. local_type_name
1. minimum_scale
1. maximum_scale
1. sql_data_type
1. sql_datetime_sub
1. num_prec_radix
1. interval_precision

## Context manager

Cursor objects do support the Python context manager syntax (the `with` statement), but it's important to understand the "context" in this scenario. The following code:
```python
with cnxn.cursor() as crsr:
    do_stuff
```
is essentially equivalent to:
```python
crsr = cnxn.cursor()
do_stuff
if not cnxn.autocommit:
    cnxn.commit()  
```
As you can see, `commit()` is called on the cursor's connection even if `autocommit` is False. Hence, the "context" is not so much the cursor itself. Rather, it's better to think of it as a database transaction that will be committed without explicitly calling `commit()`.

Note, the cursor object is not explicitly closed when the context is exited.
