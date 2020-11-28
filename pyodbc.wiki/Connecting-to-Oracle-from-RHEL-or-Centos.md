Use Oracle instant client on RHEL to connect to Oracle database. CentOS is derived from Red Hat so the driver works for CentOS as well. This driver uses unixODBC as its driver manager. The driver and driver manager must be installed globally(as root) on your server:

#### Install unixODBC

See http://www.unixodbc.org/ for reference.

Use the latest unixODBC version 2.3.4 (preferred). Download the source, http://www.unixodbc.org/download.html

As root,
```bash
cd <Download Folder>
wget ftp://ftp.unixodbc.org/pub/unixODBC/unixODBC-2.3.4.tar.gz
tar -xf unixODBC-2.3.4.tar.gz
cd unixODBC-2.3.4/
./configure -sysconfdir=/etc 1> conf_std.log 2> conf_err.log
make 1> mk_std.log 2> make_err.log
sudo make install 1> mki_std.log 2> mki_err.log
```

#### Install the Oracle Instant Client (ODBC Driver) for Linux

See http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html for reference.

Choose the Instant Client Downloads for Linux x86-64
http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html

Download: oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm , oracle-instantclient11.2-odbc-11.2.0.3.0-1.x86_64.rpm, oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm 

Note: If you need 12c instant client choose the appropriate basic, odbc and devel rpms.

As root,
```bash
cd <Download Folder> 
rpm -ivh oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
rpm -ivh oracle-instantclient11.2-odbc-11.2.0.3.0-1.x86_64.rpm
rpm -ivh oracle-instantclient11.2-devel-11.2.0.3.0-1.x86_64.rpm
```

Oracle installs the library in /usr/lib/oracle/11.2/client64/lib.
set the library path, add it to the profile (as required)
```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/11.2/client64/lib
```

##### Test Oracle Driver installation
```
dltest /usr/lib/oracle/11.2/client64/lib/libsqora.so.11.1
#SUCCESS: Loaded /usr/lib/oracle/11.2/client64/lib/libsqora.so.11.1
```

Add the oracle entry to obdcinst.ini
```bash
[MyOracle]
Description=Oracle Unicode driver
Driver=/usr/lib/oracle/11.2/client64/lib/libsqora.so.11.1
UsageCount=1
FileUsage=1
```


### Test the Connection using pyodbc
Try the connection to your database with something like this:
```bash
python -c "import pyodbc; print(pyodbc.connect('DRIVER=MyOracle;DBQ=x.x.x.x:1521/orcl;UID=myuid;PWD=mypwd'))"
```
DBQ format:Host:Port/"oracle instance"
