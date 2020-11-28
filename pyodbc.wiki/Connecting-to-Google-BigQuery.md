BigQuery is Google's analytics platform in the cloud.  The ODBC drivers for BigQuery are licensed by Google from [Simba](https://www.simba.com/drivers/bigquery-odbc-jdbc/) and can be downloaded (for free) from here: https://cloud.google.com/bigquery/partners/simba-drivers/

### Linux

For reference: https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/linux/content/odbc/intro.htm

It's important to set the correct encoding for your driver manager (iODBC or unixODBC).  In your odbcinst.ini file, set the encoding attribute `DriverManagerEncoding` according to [here](https://www.simba.com/products/SEN/doc/development_guides/nosql/content/testingandtroubleshooting/drivermanagerencoding.htm), e.g.:

```
[Simba ODBC Driver for Google BigQuery 64-bit]
Driver=/opt/simba/googlebigqueryodbc/lib/64/libgooglebigqueryodbc_sb64.so
DriverManagerEncoding=UTF-16
```

In your odbc.ini file, include the key file associated with your Service Account authentication, e.g.:
```
[BigQuery]
Driver=Simba ODBC Driver for Google BigQuery 64-bit
Catalog=<your default BigQuery project>
OAuthMechanism=0
Email=<the email address associated with the key file>
KeyFilePath=<path to the JSON file downloaded when creating the service account>
```

### Windows

For reference: https://www.simba.com/products/BigQuery/doc/ODBC_InstallGuide/win/content/odbc/bq/windows/dsn-bigquery.htm

To access BigQuery, you must use OAuth authentication, rather than username and password.  This can be either "User Authentication" or "Service Authentication".  See [here](https://cloud.google.com/bigquery/docs/authentication/) for more information.  Assuming you are using Service Authentication, you should already have a key file, and this file should be available on your PC somewhere.  The key file is a small JSON file that contains the key-value pair `"type": "service_account"`.

To set up the Windows DSN for BigQuery, open up your ODBC Data Source Administrator utility (by running odbcad32.exe), then open up the "Google BigQuery" DSN under the System DSN tab.  In there, enter your email address and the path to your key file in the Service Authentication section.  At the bottom of the form, choose a project using the dropdown.  You can choose a dataset too if you wish.  Be aware, in the Advanced button popup, you may need to check the box "Use SQL_WVARCHAR instead of SQL_VARCHAR".

Once the DSN has been created, you should be able to query BigQuery as usual, e.g.:
```python
import pyodbc
# Note, "autocommit" must be set True on the connection, otherwise you get
# the error "Transactions are not supported."
cnxn = pyodbc.connect('DSN=Google BigQuery', autocommit=True)
cursor = cnxn.cursor()
rows = cursor.execute('select * from mydataset.mytable').fetchall()
cnxn.close()
```