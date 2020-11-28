Python exceptions are raised by pyodbc when ODBC errors are detected. The exception classes specified in the [Python DB API](https://www.python.org/dev/peps/pep-0249/#exceptions "database exceptions") specification are used:


* Error
  * DatabaseError
    * DataError
    * OperationalError
    * IntegrityError
    * InternalError
    * ProgrammingError
    * NotSupportedError

When an error occurs, the type of exception raised is based on the SQLSTATE value, typically provided by the database.


SQLSTATE | Exception
-------- | ---------
 0A000   | pyodbc.NotSupportedError
 40002   | pyodbc.IntegrityError
 22***   | pyodbc.DataError
 23***   | pyodbc.IntegrityError
 24***   | pyodbc.ProgrammingError
 25***   | pyodbc.ProgrammingError
 42***   | pyodbc.ProgrammingError
 HYT00   | pyodbc.OperationalError
 HYT01   | pyodbc.OperationalError


For example, a primary key error (attempting to insert a value when the key already exists) will raise an IntegrityError.