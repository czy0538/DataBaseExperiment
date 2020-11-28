Output Converter functions offer a flexible way to work with returned results that pyodbc does not natively support. For example, Microsoft SQL Server returns values from a DATETIMEOFFSET column as SQL type -155, which does not have native support in pyodbc (and many other ODBC libraries). Simply retrieving the value ...

```python
import pyodbc
cnxn = pyodbc.connect("DSN=myDb")

crsr = cnxn.cursor()
# create test data
crsr.execute("CREATE TABLE #dto_test (id INT PRIMARY KEY, dto_col DATETIMEOFFSET)")
crsr.execute("INSERT INTO #dto_test (id, dto_col) VALUES (1, '2017-03-16 10:35:18 -06:00')")

value = crsr.execute("SELECT dto_col FROM #dto_test WHERE id=1").fetchval()
print(value)

crsr.close()
cnxn.close()
```

... results in the error

> pyodbc.ProgrammingError: ('ODBC SQL type -155 is not yet supported.  column-index=0  type=-155', 'HY106')

However, we can define an Output Converter function to decode the bytes returned, [add that function to the Connection object](Connection#add_output_converter), and then use the resulting value, e.g., 

```python
import struct
import pyodbc
cnxn = pyodbc.connect("DSN=myDb")


def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    tweaked = [tup[i] // 100 if i == 6 else tup[i] for i in range(len(tup))]
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:07d} {:+03d}:{:02d}".format(*tweaked)


crsr = cnxn.cursor()
# create test data
crsr.execute("CREATE TABLE #dto_test (id INT PRIMARY KEY, dto_col DATETIMEOFFSET)")
crsr.execute("INSERT INTO #dto_test (id, dto_col) VALUES (1, '2017-03-16 10:35:18 -06:00')")

cnxn.add_output_converter(-155, handle_datetimeoffset)
value = crsr.execute("SELECT dto_col FROM #dto_test WHERE id=1").fetchval()
print(value)

crsr.close()
cnxn.close()
```

which prints the string representation of the DATETIMEOFFSET value

```none
2017-03-16 10:35:18.0000000 -06:00
```
Or, we could use this function to create a `datetime` object

```python
def handle_datetimeoffset(dto_value):
    # ref: https://github.com/mkleehammer/pyodbc/issues/134#issuecomment-281739794
    tup = struct.unpack("<6hI2h", dto_value)  # e.g., (2017, 3, 16, 10, 35, 18, 0, -6, 0)
    return datetime(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6] // 1000,
                    timezone(timedelta(hours=tup[7], minutes=tup[8])))
```

which would return

```none
datetime.datetime(2017, 3, 16, 10, 35, 18, 0, tzinfo=datetime.timezone(datetime.timedelta(-1, 64800)))
```

### Removing an Output Converter function

To remove all Output Converter functions, simply do:

```python
cnxn.clear_output_converters()
```

To remove a single Output Converter function (new in version 4.0.25), use `remove_output_converter` like so:

```python
cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, decode_sketchy_utf16)
rows = crsr.columns("Clients").fetchall()
cnxn.remove_output_converter(pyodbc.SQL_WVARCHAR)  # restore default behaviour
```

### Temporarily replacing an Output Converter function

Starting with version 4.0.26 we can also use `get_output_converter` to retrieve the currently active Output Converter function so we can temporarily replace it and then restore it afterwards.

```python
prev_converter = cnxn.get_output_converter(pyodbc.SQL_WVARCHAR)
cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, decode_sketchy_utf16)  # temporary replacement
rows = crsr.columns("Clients").fetchall()
cnxn.add_output_converter(pyodbc.SQL_WVARCHAR, prev_converter)  # restore previous behaviour
```
