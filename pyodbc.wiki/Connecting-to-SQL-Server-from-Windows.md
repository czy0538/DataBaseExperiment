### Using an ODBC driver

Microsoft have written and distributed multiple ODBC drivers for SQL Server:

* {SQL Server} - released with SQL Server 2000
* {SQL Native Client} - released with SQL Server 2005 (also known as version 9.0)
* {SQL Server Native Client 10.0} - released with SQL Server 2008
* {SQL Server Native Client 11.0} - released with SQL Server 2012
* {ODBC Driver 11 for SQL Server} - supports SQL Server 2005 through 2014
* {ODBC Driver 13 for SQL Server} - supports SQL Server 2005 through 2016
* {ODBC Driver 13.1 for SQL Server} - supports SQL Server 2008 through 2016
* {ODBC Driver 17 for SQL Server} - supports SQL Server 2008 through 2019

Note that the "SQL Server Native Client ..." and earlier drivers are deprecated and should not be used for new development.

The connection strings for all these drivers are essentially the same, for example:
```
DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password
```
or, in Python:
```python
conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=test;DATABASE=test;UID=user;PWD=password')
```
You can find out what drivers are installed on your PC by navigating to 'Control Panel -> Administrative Tools -> Data Sources (ODBC)' and clicking on the 'Drivers' tab.  You can also get to this ODBC Administrator window by running 'odbcad32.exe'.  Be aware there are separate 32-bit and 64-bit versions of the ODBC Administrator.  Lastly, you can get the driver names programmatically by running the Python command `pyodbc.drivers()`.

It's generally best to use the latest drivers on your PC, regardless of the version of SQL Server you are connecting to, because the drivers are largely backwards-compatible.  However you may prefer to use the specific driver for your SQL Server instance.


### Using a DSN

A DSN (or Data Source Name) allows you to define the ODBC driver, server, database, login credentials (possibly), and other connection attributes all in one place, so you don't have to provide them in your connection string.  You can set up DSNs on your PC by using your ODBC Data Source Administrator window.

To get to your ODBC Data Source Administrator window, navigate to 'Control Panel -> Administrative Tools -> Data Sources (ODBC)'. Under the tabs 'User DSN' or 'System DSN' click on the 'Add...' button and follow the wizard instructions.  'User DSN' is for just you, 'System DSN' is for all users.  Choose a driver that is suitable for the version of SQL Server you are connecting to, and add any other connection information that is relevant.  Once you have created your new DSN, use it in the pyodbc.connect() function as follows:
```python
conn = pyodbc.connect('DSN=mynewdsn;UID=user;PWD=password')
```
Attributes in the connection string will override any attributes in the DSN.

### Other connection attributes
You can connect to your SQL Server instance using a trusted connection, i.e. using your Windows account rather than a login name and password, by using the Trusted_Connection attribute, e.g.:
```python
conn = pyodbc.connect('DSN=mynewdsn;Trusted_Connection=yes;')
```

Adding the APP keyword allows you to provide a descriptive label for your database connection (of up to 128 characters). 
 This is useful for database administrators, e.g.:
```python
conn = pyodbc.connect('DSN=mynewdsn;APP=Daily Incremental Backup;')
```