Those of you who come from a database background will be familiar with the idea of database transactions, i.e. where a series of SQL statements are committed together (or rolled-back) in one operation. Transactions are crucial if you need to make multiple updates to a database where each update would leave the database in an invalid or inconsistent state, albeit temporarily. The classic example of this is processing a check, where money is transferred from one bank account to another, i.e. a debit from one account and a credit to another account. It is important that both the debit and credit are committed together otherwise it will appear as if money has been (temporarily) created or destroyed.

Note, this whole article is relevant only when `autocommit` is set to False on the pyodbc connection (False is the default). When `autocommit` is set to True, the database executes a commit automatically after every SQL statement, so transaction management by the client is not possible. Note, those automatic commits are executed by the database itself, not pyodbc, i.e. the database essentially runs every SQL statement within its own transaction.

When using pyodbc with `autocommit=False`, it is important to understand that you never explicitly open a database transaction in your Python code. Instead, a database transaction is implicitly opened when a Connection object is created with `pyodbc.connect()`. That database transaction is then either committed or rolled-back by explicitly calling `commit()` or `rollback()`, at which point a new database transaction is implicitly opened. SQL statements are executed using the Cursor `execute()` function, hence the equivalent of the following SQL:
```sql
BEGIN TRANSACTION
  UPDATE T1 SET ...
  DELETE FROM T1 WHERE ...
  INSERT INTO T1 VALUES ...
COMMIT TRANSACTION
BEGIN TRANSACTION
  INSERT INTO T2 VALUES ...
  INSERT INTO T3 VALUES ...
COMMIT TRANSACTION
```
in Python would be:
```python
cnxn = pyodbc.connect('mydsn', autocommit=False)
crsr = cnxn.cursor()
crsr.execute("UPDATE T1 SET ...")
crsr.execute("DELETE FROM T1 WHERE ...")
crsr.execute("INSERT INTO T1 VALUES ...")
cnxn.commit()
crsr.execute("INSERT INTO T2 VALUES ...")
crsr.execute("INSERT INTO T3 VALUES ...")
cnxn.commit()
cnxn.close()
```
As you can see, no database transaction is ever explicitly opened using pyodbc but they are explicitly committed.

Just to re-emphasize, database transactions are managed through connections, not cursors. Cursors are merely vehicles to execute SQL statements and manage their results, nothing more. Yes, there is a convenience function `commit()` on the Cursor object but that simply calls `commit()` on the cursor's parent Connection object. Bear in mind too that when `commit()` is called on a connection, ALL the updates from ALL the cursors on that connection are committed together (ditto for `rollback()`). If you want to have separate concurrent transactions, you should probably create a separate connection object for each transaction.

Unless you positively commit a transaction, the transaction will almost certainly get rolled back eventually. For example, when a connection is closed with the `close()` function, a rollback is always issued on the connection. When a Connection object goes out of scope before it's closed (e.g. because an exception occurs), the Connection object is automatically deleted by Python, and a rollback is issued as part of the deletion process.  The default behavior is to rollback transactions so always commit your transactions.

#### Specifying a Transaction Isolation level

Database management systems that support transactions often support several levels of transaction isolation to control the effects of multiple processes performing simultaneous operations within their own transactions. ODBC supports four (4) levels of transaction isolation:

- SQL_TXN_READ_UNCOMMITTED
- SQL_TXN_READ_COMMITTED
- SQL_TXN_REPEATABLE_READ
- SQL_TXN_SERIALIZABLE

You can specify one of these in your Python code using the `Connection#set_attr` method, e.g.,

```python
cnxn = pyodbc.connect(conn_str, autocommit=True)
cnxn.set_attr(pyodbc.SQL_ATTR_TXN_ISOLATION, pyodbc.SQL_TXN_SERIALIZABLE)
cnxn.autocommit = False  # enable transactions
```

Note that a particular database engine may not support all four isolation levels. For example, Microsoft Access only supports `SQL_TXN_READ_COMMITTED`.