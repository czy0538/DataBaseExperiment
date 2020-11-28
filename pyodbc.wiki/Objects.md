The objects provided by pyodbc are defined by the [Python Database API Specification v2.0](https://www.python.org/dev/peps/pep-0249/), so you should familiarize yourself with it.

### The Module

[module documentation](The-pyodbc-Module)

You start, of course, by importing the pyodbc module:

```python
import pyodbc
```

If you can't get past this, pyodbc is not installed correctly - see the [Installing pyodbc](Install) page.

The module provides:

* The connect() function.
* Some global settings which are set on new connections: autocommit, pooling, and lowercase.
* Some informational constants: version, apilevel, threadsafety, and paramstyle.
* Lots and lots of ODBC constants such as SQL_COLLATION_SEQ, used with the SQL catalog and SQLGetInfo functions.

### Connections

[Connection documention](Connection)

The Connection object represents a single connection to the database and is obtained from the module's connect() function:

```python
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=mine;UID=me;PWD=pwd')
```

There are two primary features of the connection object:

1. You use cnxn.cursor() to create a new Cursor.
1. You use cnxn.commit() or cnxn.rollback() to commit or rollback work performed with the Cursor.

#### commit

Unless you have enabled autocommit (in the pyodbc.connect() function or with cnxn.autocommit), all uncommitted work will be discarded when the Connection object is closed. You must call cnxn.commit() or your work will be lost!
```python
cnxn = pyodbc.connect(...)
# do work here...
cnxn.commit()
cnxn.close()
```

#### exception handling

The [standard Python implementation](www.python.org) uses reference counting for garbage collection, so as long as your connection and cursors are not used outside the current function, they will be closed automatically and immediately when the function exits. Since connections automatically roll back changes (since the last commit call) when they are closed, you do not need a finally block to clean up errors:

```python
cnxn   = pyodbc.connect(...)
cursor = cnxn.cursor()
# do work here
# an exception is raised here
cnxn.commit()
```

In this example, the exception causes the function to exit without reaching the commit call. Therefore all the work performed with the cursor will be rolled back.

If your code might be ported to PyPy or other Python implementations without reference counting, you can use `try` or `with`.  Connections used in a `with` block will commit at the end of the block if no errors are raised and will rollback otherwise:

``` python
cnxn = pyodbc.connect(...)
cursor = cnxn.cursor()
with cnxn:
    cursor.execute(...)
```

### Cursors

[Cursor documentation](Cursor)

Cursor objects are used to execute SQL statements. ODBC and pyodbc allow multiple cursors per connection, but not all databases support this. You can use SQLGetInfo to determine how many concurrent cursors can be supported: `cnxn.getinfo(pyodbc.SQL_MAX_CONCURRENT_ACTIVITIES)`

The most important features of cursors are:

* the execute() function which executes SQL
* the description tuple which describes the results of a select statement
* rowcount which is the number of rows selected, updated, or deleted
* the fetch functions for accessing the resulting rows

```python
cnxn   = pyodbc.connect(...)
cursor = cnxn.cursor()

cursor.execute("""
               select user_id, last_logon
                 from users
                where last_logon > ?
                  and user_type <> 'admin'
               """, twoweeks)

rows = cursor.fetchall()

for row in rows:
    print('user %s logged on at %s' % (row.user_id, row.last_logon))
```

### Rows

[Row documentation](Row)

Row objects are tuple-like, as specified by the DB API, but also support accessing columns by name. The names of the columns is described by Cursor.description.

Row objects do not reference their creating cursor, so it is valid to use rows after closing the cursor and connection. Each row has a cursor_description attribute which is the same as the Cursor.description from the row's cursor, so it is accessible without the cursor.
