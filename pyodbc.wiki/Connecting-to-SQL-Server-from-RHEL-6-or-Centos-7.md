Microsoft provide database drivers specifically for Red Hat Enterprise to connect to SQL Server (https://msdn.microsoft.com/en-us/library/hh568451.aspx). CentOS is derived from Red Hat so the same driver will usually work with CentOS just as well. Version 13.0 works with Red Hat 6 and 7. The following instructions are for version 13 only.

> Note: Check this link ...
>
> [Installing the Microsoft ODBC Driver for SQL Server on Linux and macOS](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server)
>
> ... for the most up-to-date information on installing the ODBC driver itself.

```
# Add the RHEL 6 library for Centos-7 of MSSQL driver. Centos7 uses RHEL-6 Libraries.
sudo su 
curl https://packages.microsoft.com/config/rhel/6/prod.repo > /etc/yum.repos.d/mssql-release.repo
exit

# Uninstall if already installed Unix ODBC driver
sudo yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts

# Install the  msodbcsql unixODBC-utf16 unixODBC-utf16-devel driver
sudo ACCEPT_EULA=Y yum install msodbcsql

#optional: for bcp and sqlcmd
sudo ACCEPT_EULA=Y yum install mssql-tools
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bash_profile
echo 'export PATH="$PATH:/opt/mssql-tools/bin"' >> ~/.bashrc
source ~/.bashrc

# optional: for unixODBC development headers
sudo yum install unixODBC-devel

# the Microsoft driver expects unixODBC to be here /usr/lib64/libodbc.so.1, so add soft links to the '.so.2' files
cd /usr/lib64
sudo ln -s libodbccr.so.2   libodbccr.so.1
sudo ln -s libodbcinst.so.2 libodbcinst.so.1
sudo ln -s libodbc.so.2     libodbc.so.1

# Set the path for unixODBC
export ODBCINI=/usr/local/etc/odbc.ini
export ODBCSYSINI=/usr/local/etc
source ~/.bashrc

# Prepare a temp file for defining the DSN to your database server
vi /home/user/odbcadd.txt

[MyMSSQLServer]
Driver      = ODBC Driver 13 for SQL Server
Description = My MS SQL Server
Trace       = No
Server      = 10.100.1.10

# register the SQL Server database DSN information in /etc/odbc.ini
sudo odbcinst -i -s -f /home/user/odbcadd.txt -l

# check the DSN installation with:
odbcinst -j
cat /etc/odbc.ini

# should contain a section called [MyMSSQLServer]

# install the python driver for database connection
pip install pyodbc
```

Additionally You can check the following 2 website for connection

https://janikarhunen.fi/connecting-to-sqlserver-from-python-app-on-centos-7.html

https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server 
