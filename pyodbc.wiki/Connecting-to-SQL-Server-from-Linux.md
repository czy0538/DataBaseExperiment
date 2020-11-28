Microsoft's instructions for installing their latest ODBC drivers onto a variety of Linux/UNIX-based platforms are [here](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server).

Create a temporary text file for defining the [ODBC DSN](https://support.microsoft.com/en-ca/help/966849/what-is-a-dsn-data-source-name) (Data Source Name) to your database, something like this:

```
[MSSQLServerDatabase]
Driver      = ODBC Driver 17 for SQL Server
Description = Connect to my SQL Server instance
Trace       = No
Server      = mydbserver.mycompany.com
```
    
In that file, leave the `Driver` line exactly as specified above, except with the correct driver version.  The driver version can be found by inspecting the system-wide "odbcinst.ini" file, which is where Microsoft's installer for the ODBC driver registers itself:

```
$ cat /etc/odbcinst.ini
[ODBC Driver 17 for SQL Server]
Description=Microsoft ODBC Driver 17 for SQL Server
Driver=/opt/microsoft/msodbcsql17/lib64/libmsodbcsql-17.4.so.1.1
UsageCount=1
```

Use the driver name exactly as it appears inside the square brackets.

NOTES: 

1. Microsoft's ODBC drivers **do not** use a `Port = ` parameter. If you need to connect to a port other than the default (1433) you must append it to the `Server` argument with a comma, e.g.,

    ```
    Server      = mydbserver.mycompany.com,49242
    ```

1. Microsoft's ODBC drivers for Linux cannot resolve instance names, so this won't work from a Linux client:

    ```
    Server      = mydbserver.mycompany.com\SQLEXPRESS
    ```
    If you need to connect to a named instance you can use the (free) [sqlserverport](https://github.com/gordthompson/sqlserverport) module.

1. If you're connecting to your local database instance, use "localhost" or, if that doesn't work, try "127.0.0.1":

    ```
    Server      = 127.0.0.1
    ```

&nbsp;

After saving your temporary config file you can create a "System DSN" by using the following commands:

```bash
# register the SQL Server database DSN information in /etc/odbc.ini
sudo odbcinst -i -s -f /path/to/your/temporary/dsn/file -l

# check the DSN installation with:
cat /etc/odbc.ini   # should contain a section called [MSSQLServerDatabase]
```

If you do not have `sudo` permissions then you can create a "User DSN" like so:

```bash
# register the SQL Server database DSN information in ~/.odbc.ini
odbcinst -i -s -f /path/to/your/temporary/dsn/file -h

# check the DSN installation with:
cat ~/.odbc.ini   # should contain a section called [MSSQLServerDatabase]
```

Connecting to the server is then done like this:

    pyodbc.connect('DSN=MSSQLServerDatabase;UID=myuid;PWD=mypwd')

### OS-specific notes:

#### CentOS

CentOS is derived from RedHat, and their major version numbers (i.e. 6 and 7) match those of RedHat, so just use the instructions for the relevant version of RedHat.

#### Ubuntu

On Ubuntu you also have the option of installing the FreeTDS ODBC driver from the Ubuntu repositories. Until [this issue](https://bugs.launchpad.net/ubuntu/+source/freetds/+bug/1173083) is resolved you need to register the driver manually:

    apt install tdsodbc
    odbcinst -i -d -f /usr/share/tdsodbc/odbcinst.ini

Note also that

1. Ubuntu repositories often install rather old versions of things like ODBC drivers so you may get a version with bugs that have been fixed in newer versions.

2. Current versions of FreeTDS ODBC do not support some features like `fast_executemany` and table-valued parameters (TVPs).

3. Using pyodbc with FreeTDS is not officially supported by Microsoft, whereas using pyodbc with "ODBC Driver xx for SQL Server" *is* officially supported.