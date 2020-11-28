Vertica is essentially a fork of PostgreSQL, so a lot of what can be said about PostgreSQL applies to Vertica as well.

## Encodings

```python
# Python 3.x
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')

# Python 2.7
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setencoding(str, encoding='utf-8')
cnxn.setencoding(unicode, encoding='utf-8', ctype=pyodbc.SQL_CHAR)
```

Bear in mind, after setting up your `odbcinst.ini` and `odbc.ini` files, you will still need to set up a `vertica.ini` file (see [here](https://www.vertica.com/docs/9.2.x/HTML/Content/Authoring/ConnectingToVertica/ClientODBC/ODBCDriverSettingsForLinuxAndUnixLikePlatforms.htm)) which defines, among other things, the driver manager encoding.
