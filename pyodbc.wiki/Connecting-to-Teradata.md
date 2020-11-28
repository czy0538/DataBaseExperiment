First, you'll probably need to build pyodbc against iODBC as their drivers use it.  (You may be able to find a driver that uses unixODBC.)

If you are using UTF-8, most of the lines will be similar to other databases, but unfortunately the metadata on macOS (this may not be necessary on Linux) will return metadata (column names) in UTF-32LE.

```python
# Python 2.7
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le')
cnxn.setencoding(str, encoding='utf-8')
cnxn.setencoding(unicode, encoding='utf-8')

# Python 3.x
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-32le')
cnxn.setencoding(encoding='utf-8')
```


### Testing

You can download a free version of Teradata Express in VMWare images.  This can also be [used in VirtualBox](http://techathlon.com/how-to-run-a-vmdk-file-in-oracle-virtualbox/).