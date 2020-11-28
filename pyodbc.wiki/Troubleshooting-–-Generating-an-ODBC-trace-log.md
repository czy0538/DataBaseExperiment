Users reporting issues with pyodbc will often be asked to provide an ODBC trace log for diagnostic purposes. Fortunately, generating the log file is easy.

### Windows

Launch the 64-bit or 32-bit ODBC Administrator depending on whether you are using 64-bit or 32-bit Python:

If you are running 64-bit Python, launch

```
C:\Windows\System32\odbcad32.exe
```

If you are running 32-bit Python, launch

```
C:\Windows\SysWOW64\odbcad32.exe
```

On the "Tracing" tab, click the "Start Tracing Now" button. Details of subsequent ODBC activity will be appended to the file specified in "Log File Path".

![Windows ODBC Administrator](https://i.stack.imgur.com/29vY0.png)

### Linux

To enable ODBC tracing under Linux (unixODBC), add an `[ODBC]` section to `odbcinst.ini` and include the following two lines:

```
[ODBC]
Trace = yes
TraceFile = /tmp/odbctrace.txt
```

NOTE: A [bug](https://github.com/lurcher/unixODBC/pull/14) in unixODBC 2.3.6 and earlier can interfere with logging under some ODBC drivers (e.g., "ODBC Driver 17 for SQL Server"). Check your installed version of unixODBC with the `odbcinst -j` command and upgrade if necessary.


### General Notes

- Always review your trace logs before submitting them. They may contain your connection string, which might include the server address/port, user credentials, or other details you might not want to make public.

- Remember to turn off ODBC tracing after generating your log file. Logging ODBC activity slows down ODBC operations and the log file will quickly become very large.
