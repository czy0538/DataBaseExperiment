Note that [Python has built-in support for SQLite3](https://docs.python.org/3/library/sqlite3.html) so you may not need to use ODBC at all.

For Windows, you can get the SQLite ODBC driver [here](http://www.ch-werner.de/sqliteodbc/). Download "sqliteodbc.exe" if you are using 32-bit Python, or "sqliteodbc_w64.exe" if you are using 64-bit Python.

For Linux, check your distribution's repositories for a pre-configured version of the driver. For example, on Ubuntu 18.04 you can simply use

```
sudo apt install libsqliteodbc
```

to install the driver.

On both Windows and Linux the driver name is "SQLite3 ODBC Driver".

For the connection string, use something like

```python
cnxn = pyodbc.connect("Driver=SQLite3 ODBC Driver;Database=sqlite.db")
```