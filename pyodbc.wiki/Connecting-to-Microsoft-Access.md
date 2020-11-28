Microsoft only produces Access ODBC drivers for the Windows platform. Third-party vendors may be able to provide Access ODBC drivers for non-Windows platforms. ([This Stack Overflow answer](https://stackoverflow.com/a/25614063/2144390) also describes options for connecting to an Access database from Python on non-Windows platforms, but they do not involve pyodbc or ODBC.)

There are actually two (2) different Access ODBC drivers from Microsoft:

1. `Microsoft Access Driver (*.mdb)` - This is the older 32-bit "Jet" ODBC driver. It is included as a standard part of a Windows install. It only works with `.mdb` (not `.accdb`) files. It is also officially deprecated.

2. `Microsoft Access Driver (*.mdb, *.accdb)` - This is the newer "ACE" ODBC driver. It is not included with Windows, but it is normally included as part of a Microsoft Office install. It is also available as a free stand-alone "redistributable" [installer](https://www.microsoft.com/en-US/download/details.aspx?id=13255) for machines without Microsoft Office. There are separate 64-bit and 32-bit versions of the "ACE" Access Database Engine (and drivers), and normally one has **either** the 64-bit version **or** the 32-bit version installed. (It is possible to force both versions to exist on the same machine but it is not recommended as it can "break" Office installations. Therefore, if you already have Microsoft Office it is *highly recommended* that you use a Python environment that matches the "bitness" of the Office install.)

The easiest way to check if one of the Microsoft Access ODBC drivers is available to your Python environment (on Windows) is to do

```python
>>> import pyodbc
>>> [x for x in pyodbc.drivers() if x.startswith('Microsoft Access Driver')]
```

If you see an empty list then you are running 64-bit Python and you need to install the 64-bit version of the "ACE" driver. If you only see `['Microsoft Access Driver (*.mdb)']` and you need to work with an `.accdb` file then you need to install the 32-bit version of the "ACE" driver.

Here is an example of how to open an MS Access database:

```python
conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=C:\path\to\mydb.accdb;'
    )
cnxn = pyodbc.connect(conn_str)
crsr = cnxn.cursor()
for table_info in crsr.tables(tableType='TABLE'):
    print(table_info.table_name)
```
If you receive an error similar to: `[Microsoft][ODBC Microsoft Access Driver]General error Unable to open registry key Temporary (volatile) Ace DSN`, ways to troubleshoot:
1. Check that you use the full path to the `.accdb` file. 
2. Rename your `.accdb` file so it doesn't include any underscores (`_`).
3. Check that you have 'read' access to the `.accdb` file.
4. Check that your registry permits read access (see Microsoft's docs [here](https://docs.microsoft.com/en-us/office/troubleshoot/error-messages/fails-accessing-page-connected-access-database) except you may need to use `regedit.exe`)
5. Check that another process or application does not have an "exclusive" lock on the file (see a Stackoverflow for Java's pyodbc [here](https://stackoverflow.com/questions/26244425/general-error-unable-to-open-registry-key-temporary-volatile-from-access)). 

## Unit Tests

There are unit tests for Python 2 and 3: `tests2\accesstests.py` and `tests3\accesstests.py`

For each, you need to pass in the name of an access file that can be used.  Empty ones you can test with are provided: `tests2\empty.mdb` and `tests2\empty.accdb`.

## Access Info

[Microsoft Access Specifications and Limitations](http://office.microsoft.com/en-ca/access-help/access-2010-specifications-HA010341462.aspx)
