#### Requirements

1. An ODBC driver manager like unixODBC or iODBC

Install unixodbc
```bash
sudo apt -y install unixodbc-dev
```
OR

To build from the source, see http://www.unixodbc.org/

Download the source, http://www.unixodbc.org/download.html

```bash
cd <Download Folder>
wget http://www.unixodbc.org/unixODBC-2.3.7.tar.gz
tar -xf unixODBC-2.3.7.tar.gz
cd unixODBC-2.3.7
./configure -sysconfdir=/etc 1> conf_std.log 2> conf_err.log
make 1> mk_std.log 2> make_err.log
sudo make install 1> mki_std.log 2> mki_err.log
``` 

2. Package libsasl2-modules-gssapi-mit

Install SASL2 package
```bash
sudo apt -y install libsasl2-modules-gssapi-mit:amd64
```


#### Install the Hive ODBC driver
Download the Hive ODBC driver from Hortonworks or Cloudera

https://hortonworks.com/downloads/#sandbox

https://www.cloudera.com/downloads/connectors/hive/odbc/2-6-1.html

```bash
wget https://public-repo-1.hortonworks.com/HDP/hive-odbc/2.1.16.1023/Debian/hive-odbc-native_2.1.16.1023-2_amd64.deb
sudo dpkg -i hive-odbc-native_2.1.16.1023-2_amd64.deb
```

Verify the driver installation; Check the directory "/usr/lib/hive/lib/native/Linux-amd64-64" 

#### Test the installation
```python3
import pyodbc

# Refer /usr/lib/hive/lib/native/hiveodbc/Setup/odbc.ini for the connection string options
# And the ODBC driver reference guides highlighted in the additional references section below
cnxnstr = 'Driver={/usr/lib/hive/lib/native/Linux-amd64-64/libhortonworkshiveodbc64.so};HIVESERVERTYPE=2;HOST=<hostname/IP>;PORT=<port>;UID=<userid>;SCHEMA=<schemaname>;AuthMECH=2'

# autocommit=True is required, else we get an error
# pyodbc.Error: ('HYC00', '[HYC00] [Hortonworks][ODBC] (11470) Transactions are not supported. (11470) (SQLSetConnnectAttr(SQL_ATTR_AUTOCOMMIT))')
cnxn = pyodbc.connect(cnxnstr, autocommit=True)

crsr = cnxn.cursor()
crsr.execute('select count(*) from tableX;')
print(crsr.fetchall())
```

#### Additional References
https://hortonworks.com/wp-content/uploads/2014/05/Product-Guide-HDP-2.1-v1.01.pdf

https://www.cloudera.com/content/www/en-us/documentation/other/connectors/hive-odbc/2-5-12/Cloudera-ODBC-Driver-for-Apache-Hive-Install-Guide-2-5-12.pdf

https://community.hortonworks.com/articles/53374/hive-odbc-setup-with-unixodbc-and-debug-logging.html
