The following instructions assume you already have a SQL Server database running somewhere that your Mac has network access to.  Just FYI, Microsoft's instructions for installing the latest drivers are [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).

#### Install FreeTDS and unixODBC

The connection to SQL Server will be made using the unixODBC driver manager and the FreeTDS driver. Installing them is most easily done using `homebrew`, the Mac package manager:

```
brew update
brew install unixodbc freetds
```

#### Edit the freetds.conf configuration file

Ensure the `freetds.conf` file is located in directory `/usr/local/etc/`, which will be a symlink to the actual file as installed by Homebrew.  Check the specific location of the `freetds.conf` file by running `tsql -C`.  The default file already contains a standard example configuration, but all you need to do is add your server information to the end, as follows:

```
[MYMSSQL]
host = mssqlhost.xyz.com
port = 1433
tds version = 7.3
```
There are other key/value pairs that can be added but this shouldn't usually be necessary, see [here](http://www.freetds.org/userguide/freetdsconf.htm) for details. The `host` parameter should be either the network name (or IP address) of the database server, or "localhost" if SQL Server is running directly on your Mac (e.g. using [Docker](https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-docker)).  A TDS version of 7.3 should be OK for SQL Server 2008 and newer, but bear in mind you might need a different value for older versions of SQL Server.  For more information on TDS protocol versions see [Choosing a TDS protocol version](http://www.freetds.org/userguide/choosingtdsprotocol.htm).  Do not use TDS versions 8.0 or 9.0 though.  Oddly, they are not newer than version 7.4.  They are actually obsolete aliases for older TDS versions and their use is discouraged.

Test the connection using the `tsql` utility, e.g. `tsql -S MYMSSQL -U myuser -P mypassword`.  If this works, you should see the following:

```
locale is "en_US.UTF-8"
locale charset is "UTF-8"
using default charset "UTF-8"
1>
```
At this point you can run SQL queries, e.g. "SELECT @@VERSION" but you'll need to enter "GO" on a separate line to actually execute the query.  Type `exit` to get out of the interactive session.

#### Edit the odbcinst.ini and odbc.ini configuration files

Run `odbcinst -j` to get the location of the `odbcinst.ini` and `odbc.ini` files (probably in the directory `/usr/local/etc/`). Edit `odbcinst.ini` to include the following:

```
[FreeTDS]
Description=FreeTDS Driver for Linux & MSSQL
Driver=/usr/local/lib/libtdsodbc.so
Setup=/usr/local/lib/libtdsodbc.so
UsageCount=1
```

Edit `odbc.ini` to include the following:

```
[MYMSSQL]
Description         = Test to SQLServer
Driver              = FreeTDS
Servername          = MYMSSQL
```
Note, the "Driver" is the name of the entry in `odbcinst.ini`, and the "Servername" is the name of the entry in `freetds.conf` (not a network name). There are other key/value pairs that can be included, see [here](http://www.freetds.org/userguide/odbcconnattr.htm) for details.

Check that all is OK by running `isql MYMSSQL myuser mypassword`. You should see the following:

```
+---------------------------------------+
| Connected!                            |
|                                       |
| sql-statement                         |
| help [tablename]                      |
| quit                                  |
|                                       |
+---------------------------------------+
```
You can enter SQL queries at this point if you like.  Type `quit` to exit the interactive session.

#### Connect with pyodbc

It should now be possible to connect to your SQL Server database using pyodbc, for example:
```
import pyodbc
# the DSN value should be the name of the entry in odbc.ini, not freetds.conf
conn = pyodbc.connect('DSN=MYMSSQL;UID=myuser;PWD=mypassword')
crsr = conn.cursor()
rows = crsr.execute("select @@VERSION").fetchall()
print(rows)
crsr.close()
conn.close()
```


#### Connecting without defining a DSN

If you don't want to define a DSN in `odbc.ini`, you can reference the driver entry you added to `odbcinst.ini`.

E.g.:

```python
cnx = pyodbc.connect(
    server="my-server.com",
    database="mydb",
    user='myuser',
    tds_version='7.4',
    password="mypassword",
    port=1433,
    driver='FreeTDS'
)
```

Note: in this case you may need to specify all necessary TDS parameters in `pyodbc.connect`.

#### Connecting without modifying `odbcinst.ini` or `odbc.ini`

If you want to avoid modifying both `odbc.ini` and `odbcinst.ini`, you can just specify the driver file location in the `driver` param in `pyodbc.connect`.

E.g.:

```python
cnx = pyodbc.connect(
    server="my-server.com",
    database="mydb",
    user='myuser',
    tds_version='7.4',
    password="mypassword",
    port=1433,
    driver='/usr/local/lib/libtdsodbc.so'
)
```
