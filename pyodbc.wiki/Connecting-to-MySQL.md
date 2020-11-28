The official reference for MySQL Connector/ODBC is [here](http://dev.mysql.com/doc/connector-odbc/en/index.html).

Connection string example:

```python
connection_string = (
    'DRIVER=MySQL ODBC 8.0 ANSI Driver;'
    'SERVER=localhost;'
    'DATABASE=mydb;'
    'UID=root;'
    'PWD=mypassword;'
    'charset=utf8mb4;'
)
```

Note: "ANSI" is not a typo. For full `utf8mb4` support including supplementary characters (like emoji) you need to use the "ANSI" version of the driver, not the "Unicode" one. See [this MySQL Connector/ODBC issue](https://bugs.mysql.com/bug.php?id=69021) for more information.

Also Note: Be certain to **not** put any spaces around the equals signs (=) when creating the connection string (as shown above), otherwise you will receive errors about not being able to find the data source name or that no default driver was specified.
  
### Encodings

MySQL uses a single encoding for all text data which you will need to configure after connecting.  The example below is for UTF-8:

```
# Python 2.7
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(str, encoding='utf-8')
cnxn.setencoding(unicode, encoding='utf-8', ctype=pyodbc.SQL_CHAR)

# Python 3.x
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')
```

You may need to add the `charset` keyword to your connection string as in the example above.

### Socket Errors on OS/X

Some MySQL ODBC drivers have the wrong socket path on OS/X, causing an error like "Can't connect to local MySQL server through socket /tmp/mysql.sock". To connect, determine the correct path and pass it to the driver using the 'socket' keyword.

Run `mysqladmin version` and look for the Unix socket entry:
```
Server version          5.0.67
Protocol version        10
Connection              Localhost via UNIX socket
UNIX socket             /var/lib/mysql/mysql.sock
```
Pass the socket path in the connection string:
```python
cnxn = pyodbc.connect('DRIVER={MySQL};DATABASE=test;SOCKET=/var/lib/mysql/mysql.sock')
```
