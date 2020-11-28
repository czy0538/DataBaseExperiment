Opening a connection to a Microsoft Excel spreadsheet (e.g. \*.xls) is achieved using the Microsoft Excel driver, typically called "Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)". Unfortunately, this driver is available only on Windows, not Unix. 

The easiest way to check if the driver is available to your Python environment (on Windows) is to use

```python
>>> import pyodbc
>>> [x for x in pyodbc.drivers() if x.startswith('Microsoft Excel Driver')]
```

The resulting list will show any matching drivers, e.g.,

```none
['Microsoft Excel Driver (*.xls)', 'Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)']
```

You can also check for the driver on your PC by navigating to Control Panel -> Administrative Tools -> Data Sources (ODBC), and then click on the "Drivers" tab. The Excel driver will be listed there, if it is installed. It may have a slightly different name. Note also that there are separate 64-bit and 32-bit versions of the ODBC Administrator utility (odbcad32.exe).

The Microsoft Excel driver does not support transactions, so you must set `autocommit` to `True` on the connection or else you will get an error, e.g.:

```none
conn_str = (
    r'DRIVER={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};'
    r'DBQ=C:\path\to\myspreadsheet.xls;'
    )
cnxn = pyodbc.connect(conn_str, autocommit=True)
crsr = cnxn .cursor()
for worksheet in crsr.tables():
    print(worksheet)
```

Excel defaults to a read-only connection, so if you want to update the spreadsheet include `ReadOnly=0` in your connection string:

```none
conn_str = (
    r'Driver={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};'
    r'DBQ=C:\path\to\myspreadsheet.xls;'
    r'ReadOnly=0'
    )
cnxn = pyodbc.connect(conn_str, autocommit=True)
```

Be careful of the data types in your Excel spreadsheet.  The Excel driver uses the most common data type from the first 8 rows of the spreadsheet to determine the data type of each column.  So if you have 5 numbers and 3 text values in the first rows of a column, the column will be considered numeric, and the 3 text values will be returned as NULL!

Also, the driver may treat the first row of the worksheet as the column names, rather than data, so be aware of this.

Overall though, it has to be said, Excel is not best suited for being accessed with an ODBC connection. You may want to consider using some other Python module instead of pyodbc, for example [xlrd](https://pypi.python.org/pypi/xlrd).