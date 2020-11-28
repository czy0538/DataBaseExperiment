# Deprecated

Please go to the project's [Release Notes](https://github.com/mkleehammer/pyodbc/releases) page.  This page will not be maintained and will be deleted in the near future.  It was created before GitHub officially supported releases.

# Archive

### 4.0.2 / 2017-01-19

Fixed parsing of decimal/numeric columns.  Because most drivers fail to create binary decimal structures pyodbc uses text.  The configured encodings were not being used for this.

### 4.0.1 / 2017-01-13
Bug fixes.

### 4.0.0 / 2016-12-30
Unicode handling rewritten for correctness.

**IMPORTANT:** The source tarball is no longer available on PyPI.  (I tried to upload a corrected version and that is not allowed.). Please upgrade.

### 3.0.10 - 2015-04-29
Binary distributions for OS X and Windows are now uploaded to PyPI and can now be installed using pip. Source distributions are also uploaded and can be used by other platforms to compile. (PyPI only allows binary uploads for OS X and Windows.)

Moved the project from Google Code hosting to GitHub. (Google is closing its open source hosting.)

Fixed potential load failure.

Fixed decimal and int issues on 64-bit linux.

Assume unixODBC rather than iODBC on OS X.

### 3.0.7 - 2013-05-19
Added context manager support to Cursor.

Added padding for driver bugs writing an extra byte.

Cursor.executemany() now accepts an iterator or generator.

Compilation improvements for FreeBSD, Cygwin, and OS/X.

Use SQL_DATA_AT_EXEC instead of SQL_DATA_LEN_AT_EXEC when possible for driver compatibility.

Row objects can now be pickled.

### 3.0.6 - 2012-06-25
Added Cursor.commit() and Cursor.rollback(). It is now possible to use only a cursor in your code instead of keeping track of a connection and a cursor.

Added `readonly` keyword to pyodbc.connect(). If set to True, SQLSetConnectAttr SQL_ATTR_ACCESS_MODE is set to SQL_MODE_READ_ONLY. This may provide better locking semantics or speed for some drivers.

Fixed an error reading SQL Server XML data types longer than 4K.

### 3.0.5 - 2012-02-23
Fixed "function sequence" errors caused by prepared SQL not being cleared ("unprepared") when a catalog function is executed.

### 3.0.4 - 2012-01-13
Fixed building on Python 2.5. Other versions are not affected.

### 3.0.3 - 2011-12-28
Update to build using gcc 4.6.2: A compiler warning was changed to an error in 4.6.2.

### 3.0.2 - 2011-12-26
This is the first official pyodbc release that supports both Python 2 and Python 3 (3.2+). Merry Christmas!

Many updates were made for this version, particularly around Unicode support. If you have outstanding issues from the 2.1.x line, please retest with this version.