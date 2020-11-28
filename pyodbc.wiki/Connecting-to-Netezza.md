These unicode connection settings should work with Netezza:

```python
# Python 2.7
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
cnxn.setencoding(str, encoding='utf-8')
cnxn.setencoding(unicode, encoding='utf-8')

# Python 3.x
cnxn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
cnxn.setencoding(encoding='utf-8')
```
If you find that columns names do not decode correctly in Python 3.x, replace
```python
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-8')
```
with
```python
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')
```

### Workaround for \x00 byte codes in Error Messages  
Set UnicodeTranslationOption in ~/.odbcinst.ini to utf16:
```
UnicodeTranslationOption = utf16
```
and
```python
cnxn.setdecoding(pyodbc.SQL_WMETADATA, encoding='utf-16le')
```