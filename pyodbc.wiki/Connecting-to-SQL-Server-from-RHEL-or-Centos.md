Microsoft provide database drivers specifically for Red Hat Enterprise to connect to SQL Server (https://msdn.microsoft.com/en-us/library/hh568451.aspx).  CentOS is derived from Red Hat so the same driver will usually work with CentOS just as well. There are actually two Microsoft drivers, versioned as numbers 11 and 13.0. Version 11 works with Red Hat 5 and 6.  Version 13.0 works with Red Hat 6 and 7. However the following instructions are for version 11 only.

Note, Microsoft driver 11 uses unixODBC as its driver manager, not FreeTDS or iODBC. Furthermore, the driver and driver manager must be installed globally on your server. Don't try installing them in a Python virtual environment, it'll end in tears.

#### Install unixODBC

See https://msdn.microsoft.com/en-us/library/hh568449.aspx#Anchor_1 for reference.

Microsoft specifies that unixODBC version 2.3.0 should be installed with their driver, and goes on to say that version 2.3.1 is not supported.  However, you should be aware that version 2.3.0 is quite old now and has some significant bugs in it, particularly when making multiple connections to the same database. That specific scenario can cause segmentation faults in your Python code - see "Driver version was not being held when a second connection was made to the driver" on http://www.unixodbc.org/ - an issue that was fixed in version 2.3.1. Hence, if you are using multiple concurrent database connections, you should definitely consider installing at least version 2.3.1 of unixODBC. The rest of these instructions assume version 2.3.2 is being installed.
```bash
# download and unzip the unixODBC driver
curl -O 'ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.2.tar.gz'
tar -xz -f unixODBC-2.3.2.tar.gz
cd unixODBC-2.3.2

# remove any existing unixODBC drivers - be very careful with 'sudo rm'!
sudo rm /usr/lib64/libodbc*

# install the unixODBC driver
# note, adding "--enable-stats=no" here is not specified by Microsoft
export CPPFLAGS="-DSIZEOF_LONG_INT=8"
./configure --prefix=/usr --libdir=/usr/lib64 --sysconfdir=/etc --enable-gui=no --enable-drivers=no --enable-iconv --with-iconv-char-enc=UTF8 --with-iconv-ucode-enc=UTF16LE --enable-stats=no 1> configure_std.log 2> configure_err.log
make 1> make_std.log 2> make_err.log
sudo make install 1> makeinstall_std.log 2> makeinstall_err.log

# the Microsoft driver expects unixODBC to be here /usr/lib64/libodbc.so.1,
# so add soft links to the '.so.2' files
cd /usr/lib64
sudo ln -s libodbccr.so.2   libodbccr.so.1
sudo ln -s libodbcinst.so.2 libodbcinst.so.1
sudo ln -s libodbc.so.2     libodbc.so.1
```
Check the unixODBC installation with the following commands. They should all return information that can be verified as correct:
```bash
ls -l /usr/lib64/libodbc*
odbc_config --version --longodbcversion --cflags --ulen --libs --odbcinstini --odbcini
odbcinst -j
isql --version
```

#### Install the Microsoft ODBC Driver for Linux

See https://msdn.microsoft.com/en-us/library/hh568454.aspx#Anchor_1 for reference.

First of all, go to https://www.microsoft.com/en-us/download/details.aspx?id=36437 and download the appropriate zip file to your Linux server.  Then install it as follows:

```bash
cd /path/to/your/driver/file/directory
tar -xz -f msodbcsql-11.0.2270.0.tar.gz
cd msodbcsql-11.0.2270.0
sudo ./install.sh install --accept-license --force 1> install_std.log 2> install_err.log
```

Check the msodbc installation with the following commands. They should all return information that can be verified as correct:

```bash
ls -l /opt/microsoft/msodbcsql/lib64/
dltest /opt/microsoft/msodbcsql/lib64/libmsodbcsql-11.0.so.2270.0 SQLGetInstalledDrivers
cat /etc/odbcinst.ini   # should contain a section called [ODBC Driver 11 for SQL Server]
```

Prepare a file for defining the DSN to your database with a temporary file something like this:    

```
[MySQLServerDatabase]
Driver      = ODBC Driver 11 for SQL Server
Description = My MS SQL Server
Trace       = No
Server      = mydbserver.mycompany.com
```
    
In that file, leave the 'Driver' line exactly as specified above, but modify the rest of the file as necessary.  Then run the following commands:

```bash
# register the SQL Server database DSN information in /etc/odbc.ini
sudo odbcinst -i -s -f /path/to/your/temporary/dsn/file -l

# check the DSN installation with:
cat /etc/odbc.ini   # should contain a section called [MySQLServerDatabase]
```

#### Test the Connection

Try connecting to your database with something like this:

```bash
python -c "import pyodbc; print(pyodbc.connect('DSN=MySQLServerDatabase;UID=myuid;PWD=mypwd'))"
```