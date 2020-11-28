For reference, the Python DB API for database modules is [here](https://www.python.org/dev/peps/pep-0249/#module-interface).

## pyodbc Attributes

All these attributes can be read, e.g. `pyodbc.version` and some can be set, e.g. `pyodbc.pooling = False`.

### version

The module version string in *major.minor.patch* format such as `4.0.25`.

### apilevel

The string constant `2.0` indicating this module supports the DB API level 2.0.

### lowercase

A Boolean that controls whether column names in result rows are lowercased. This can be changed
any time and affects queries executed after the change. The default is `False`. This can be
useful when database columns have inconsistent capitalization.

### native_uuid

A Boolean that determines whether SQL_GUID columns, e.g. UNIQUEIDENTIFIER or UUID, are returned
as text (with `False`, the default) or as `uuid.UUID` objects (with `True`).  The default is False for
backwards compatibility, but this may change in a future release.

### pooling

A Boolean indicating whether connection pooling is enabled. This is a global (HENV) setting, so
it can only be modified before the first connection is made. The default is `True`, which
enables ODBC connection pooling.

### threadsafety

The value `1`, indicating that threads may share the module but not connections. Note that
connections and cursors may be used by different threads, just not at the same time.

### paramstyle

The string constant `qmark` to indicate parameters are identified using question marks.

## pyodbc Functions

### connect()

    connect(*connstring, autocommit=False, timeout=0, readonly=False,
            attrs_before=None, encoding='utf-16le', ansi=False, **kwargs)

Creates and returns a new connection to the database, e.g.:

    cnxn = pyodbc.connect('DSN=SQLServer1;Database=test;UID=me;PWD=mypwd', autocommit=True)

To create a connection to a database, pyodbc
[passes](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function)
an "ODBC connection string" to the local driver manager (e.g. unixODBC or odbc32.dll) which
then calls the relevant database driver which in turn calls the database to request a connection.
Hence, this ODBC connection string must
[include](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqldriverconnect-function#comments)
all the necessary connection information.  This information is formatted as key/value pairs separated
by semi-colons (the values can be enclosed with curly braces if necessary), e.g.:

    driver={PostgreSQL Unicode};server=localhost;database=test;uid=me;pwd=mypwd

The `connect()` function constructs this ODBC connection string by concatenating the
`connstring` parameter with key/value pairs from the kwargs.
(Python 2 accepts both ANSI and Unicode strings.)
Both `connstring` and the kwargs are optional, but one of them must be provided.
Note, `connect()` does not attempt to parse any key/value pairs in the `connstring`
parameter.  It uses that string exactly as given.
Hence, the call:

    connect('DSN=MySQLDB;SCHEMA=DW', UID='me', PWD='mypwd')

will cause `connect()` to generate an ODBC connection string of:

    DSN=MySQLDB;SCHEMA=DW;UID=me;PWD=mypwd

This string is then used to create the connection.

The relevant connection keywords vary from database to database but are generally similar.
See [here](https://www.connectionstrings.com/) for examples.  Typically, the keywords are
case-insensitive but this depends on the database driver.
Note, some kwarg keywords are converted by pyodbc to ODBC equivalents.

#### converted kwarg keywords

The DB API [recommends](https://www.python.org/dev/peps/pep-0249/#footnotes) the use of certain
keywords that are not typically used in ODBC connection strings, so as a convenience when these
keywords are provided as kwargs, the `connect()` function converts them to ODBC-style equivalents,
as follows:

kwarg keyword | is converted to
--------------|----------------
host          | server
user          | uid
password      | pwd

Hence, the call:

    connect('driver=MySQL', host='my1.xyz.com', database='DB1', user='admin', password='mypwd')

will generate an ODBC connection string of:

    driver=MySQL;server=my1.xyz.com;database=DB1;uid=me;pwd=mypwd

#### other parameters

parameter | notes | default
------- | ----- | -------
ansi | If True, indicates the driver does not support Unicode. | False
attrs_before | A dictionary of connection attributes to set before connecting. |
autocommit | If True, causes a commit to be performed after each SQL statement. | False
encoding | The encoding for the connection string. | utf-16le
readonly | If True, the connection is set to read-only. | False
timeout | The timeout for the connection attempt, in seconds. |

##### ansi

The `ansi` parameter should only be used to work around driver bugs. pyodbc will determine if the
Unicode connection function (SQLDriverConnectW) exists and will always attempt to call it. If the
driver returns IM001 indicating it does not support the Unicode version, the ANSI version is
tried (SQLDriverConnectA). Any other SQLSTATE is turned into an exception. Setting `ansi` to True
skips the Unicode attempt and only connects using the ANSI version. This is useful for drivers
that return the wrong SQLSTATE (or if pyodbc is out of date and should support other SQLSTATEs).

##### attrs_before

The `attrs_before` parameter is an optional dictionary of connection attributes.  These
will be set on the connection via
[SQLSetConnectAttr](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlsetconnectattr-function)
before a connection is attempted.

The dictionary keys must be the integer constants defined by ODBC or the driver.
The dictionary values can be integers, bytes, bytearrays, or strings.
Below is an example that sets the SQL_ATTR_PACKET_SIZE
connection attribute to 32K.

    SQL_ATTR_PACKET_SIZE = 112
    cnxn = connect(cstring, attrs_before={ SQL_ATTR_PACKET_SIZE : 1024 * 32 })

##### autocommit

If `autocommit` is False, database transactions must be explicitly committed (with
[cnxn.commit()](Connection#commit)). Most of the time, you will probably want to set this
to True.
Note, when True, it's the database that executes a commit after each SQL statement, not pyodbc.

##### encoding

The ODBC connection string must be sent to the driver as a byte sequence, hence the Python
string must first be encoded using the named
[encoding](https://docs.python.org/3/library/codecs.html#standard-encodings).

##### readonly

This causes the connection's
[SQL_ATTR_ACCESS_MODE](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlsetconnectattr-function)
attribute to be set to read-only (SQL_MODE_READ_ONLY) before the connection occurs.
Not all drivers and/or databases support this.

##### timeout

This causes the connection's
[SQL_ATTR_LOGIN_TIMEOUT](https://docs.microsoft.com/en-us/sql/odbc/reference/syntax/sqlsetconnectattr-function)
attribute to be set before the connection is attempted.
If the connection cannot be established within the given timeout (in seconds), an `OperationalError`
exception will be raised.  Note, this timeout functionality is implemented by the database driver,
not pyodbc, and not all drivers support this.

### dataSources()

    dataSources() -> { DSN : Description }

Returns a dictionary of the available DSNs and their descriptions.

On Windows, these will be the ones defined in the [ODBC Data Source Administrator](https://msdn.microsoft.com/en-us/library/ms188691.aspx) and will be specific to the bitness of the Python being run (i.e. 32-bit or 64-bit).
On Unix, these will be the ones defined in the user's odbc.ini file (typically ~/.odbc.ini) and/or the system odbc.ini file (typically /etc/odbc.ini).

Note: unixODBC may have a bug that only returns items from the users odbc.ini file without
merging the system one.

### drivers()

    drivers() -> [ DriverName1, DriverName2, ... DriverNameN ]

Returns a list of ODBC Drivers that are available to pyodbc.

On Windows, this list will be specific to the bitness of the Python being run (i.e. 32-bit or 64-bit).

### TimeFromTicks()

    t = pyodbc.TimeFromTicks(tics)

Returns a datetime.time object initialized from the given ticks value (number of seconds since
the epoch; see the documentation of the standard Python time module for details).

### DateFromTicks()

    d = pyodbc.DateFromTicks(d)
    
Returns a datetime.date object initialized from the given ticks value (number of seconds since
the epoch; see the documentation of the standard Python time module for details).

### TimestampFromTicks()

    dt = pyodbc.TimestampFromTicks(d)
    
Returns a datetime.datetime object initialized from the given ticks value (number of seconds since
the epoch; see the documentation of the standard Python time module for details).

### setDecimalSeparator()

    pyodbc.setDecimalSeparator('.')

Sets the decimal separator character used when parsing NUMERIC/DECIMAL values from the
database, e.g. the "." in "1,234.56".  The default is to use the current locale's
"[decimal_point](https://docs.python.org/3/library/locale.html#locale.localeconv)"
value when pyodbc was first imported, or "." if the locale is not available.
This function overrides the default.

### getDecimalSeparator()

    print(pyodbc.getDecimalSeparator())
    
Returns the decimal separator character used when parsing NUMERIC/DECIMAL values from the database.
