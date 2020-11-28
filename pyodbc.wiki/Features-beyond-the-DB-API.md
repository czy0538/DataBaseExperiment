### Introduction
The following features are beyond the requirements of [DB API 2.0](https://www.python.org/dev/peps/pep-0249/). They are intended to provide a very Python-like, convenient programming experience, but you should not use them if your code needs to be portable between DB API modules. (Though I hope future DB API specifications will adopt some of these features.)

### fetchval

The `fetchval()` convenience method returns the first column of the first row if there are results, otherwise it returns None.

    count = cursor.execute('select count(*) from users').fetchval()

### fast_executemany

(New in version 4.0.19.) Simply adding

```python
# crsr is a pyodbc.Cursor object
crsr.fast_executemany = True
```

can boost the performance of `executemany` operations by greatly reducing the number of round-trips to the server. 

Notes: 
- This feature is "off" by default, and is currently only recommended for applications that use Microsoft's ODBC Driver for SQL Server. 
- The parameter values are held in memory, so very large numbers of records (tens of millions or more) may cause memory issues.
- Writing fractional seconds of `datetime.time` values is supported, unlike normal pyodbc [behavior](https://github.com/mkleehammer/pyodbc/wiki/Tips-and-Tricks-by-Database-Platform#time-columns)
- See [this tip](https://github.com/mkleehammer/pyodbc/wiki/Tips-and-Tricks-by-Database-Platform#using-fast_executemany-with-a-temporary-table) regarding fast_executemany and temporary tables.
- For information on using fast_executemany with SQLAlchemy (and pandas) see the Stack Overflow question [here](https://stackoverflow.com/q/48006551/2144390).

### Access Values By Name
The DB API specifies that results must be tuple-like, so columns are normally accessed by indexing into the sequence (e.g. `row[0]`) and pyodbc supports this. However, columns can also be accessed by name:
```python
cursor.execute("select album_id, photo_id from photos where user_id=1")
row = cursor.fetchone()
print(row.album_id, row.photo_id)
print(row[0], row[1])  # same as above, but less readable
```
This makes the code easier to maintain when modifying SQL, more readable, and allows rows to be used where a custom class might otherwise be used. All rows from a single execute share the same dictionary of column names, so using Row objects to hold a large result set may also use less memory than creating a object for each row.

The SQL "as" keyword allows the name of a column in the result set to be specified. This is useful if a column name has spaces or if there is no name:
```python
cursor.execute("select count(*) as photo_count from photos where user_id < 100")
row = cursor.fetchone()
print(row.photo_count)
```
### Rows Values Can Be Replaced
Though SQL is very powerful, values sometimes need to be modified before they can be used. Rows allow their values to be replaced, which makes them even more convenient ad-hoc data structures.
```python
# Replace the 'start_date' datetime in each row with one that has a time zone.
rows = cursor.fetchall()
for row in rows:
    row.start_date = row.start_date.astimezone(tz)
```
Note that columns cannot be added to rows; only values for existing columns can be modified.

### Cursors are Iterable
The DB API makes this an optional feature. Each iteration returns a row object.
```python
cursor.execute("select album_id, photo_id from photos where user_id=1")
for row in cursor:
    print(row.album_id, row.photo_id)
```
### Cursor.execute() Returns the Cursor
The DB API specification does not specify the return value of Cursor.execute(). Previous versions of pyodbc (2.0.x) returned different values, but the 2.1+ versions always return the Cursor itself.

This allows for compact code such as:
```python
for row in cursor.execute("select album_id, photo_id from photos where user_id=1"):
    print(row.album_id, row.photo_id)

row  = cursor.execute("select * from tmp").fetchone()
rows = cursor.execute("select * from tmp").fetchall()

count = cursor.execute("update photos set processed=1 where user_id=1").rowcount
count = cursor.execute("delete from photos where user_id=1").rowcount
```
### Passing Parameters
As specified in the DB API, Cursor.execute() accepts an optional sequence of parameters:
```python
cursor.execute("select a from tbl where b=? and c=?", (x, y))
```
However, this seems complicated for something as simple as passing parameters, so pyodbc also accepts the parameters directly. Note in this example that x & y are not in a tuple:
```python
cursor.execute("select a from tbl where b=? and c=?", x, y)
```
### Autocommit Mode
The DB API specifies that connections require a manual commit and pyodbc complies with this. However, connections also support autocommit, using the autocommit keyword of the connection function or the autocommit attribute of the Connection object:
```python
cnxn = pyodbc.connect(cstring, autocommit=True)
```
or
```python
cnxn.autocommit = True
cnxn.autocommit = False
```
### Lowercase
Setting `pyodbc.lowercase=True` will cause all column names in rows to be lowercased. Some people find this easier to work with, particularly if a database has a mix of naming conventions. If your database is case-sensitive, however, it can cause some confusion.

### Connection Pooling
ODBC connection pooling is turned on by default. It can be turned off by setting `pyodbc.pooling=False` before any connections are made.

### Query Timeouts
The Connection.timeout attribute can be set to a number of seconds after which a query should raise an error. The value is in seconds and will cause an OperationalError to be raised with SQLSTATE HYT00 or HYT01. By default the timeout value is 0 which disables the timeout.

### Miscellaneous ODBC Functions
Most of the ODBC catalog functions are available as methods on Cursor objects. The results are presented as SELECT results in rows that are fetched normally. The Cursor page documents these, but it may be helpful to refer to Microsoft's ODBC documentation for more details.

For example:
```python
cnxn   = pyodbc.connect(...)
cursor = cnxn.cursor()
for row in cursor.tables():
    print(row.table_name)
```
| ODBC Function | Method | Description |
|---------------|--------|-------------|
| SQLTables | Cursor.tables | Returns a list of table, catalog, or schema names, and table types. |
| SQLColumns | Cursor.columns | Returns a list of column names in specified tables. |
| SQLStatistics | Cursor.statistics | Returns a list of statistics about a single table and the indexes associated with the table. |
| SQLSpecialColumns | Cursor.rowIdColumns | Returns a list of columns that uniquely identify a row. |
| SQLSpecialColumns | Cursor.rowVerColumns | Returns a list of columns that are automatically updated when any value in the row is updated. |
| SQLPrimaryKeys | Cursor.primaryKeys | Returns a list of column names that make up the primary key for a table. |
| SQLForeignKeys | Cursor.foreignKeys | Returns a list of column names that are foreign keys in the specified table (columns in the specified table that refer to primary keys in other tables) or foreign keys in other tables that refer to the primary key in the specified table. |
| SQLProcedures | Cursor.procedures | Returns information about the procedures in the data source. |
| SQLProcedures | Cursor.getTypeInfo | Returns a information about the specified data type or all data types supported by the driver. |
