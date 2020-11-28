import pyodbc

# 连接建立区
server = 'SMALLBLACK\SQLEXPRESS'
database = 'ST'
username = 'sa'
password = '19991104'
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                       SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password)
# end

cursor = cnxn.cursor()  # 游标
cursor.execute("SELECT * from s;")
row = cursor.fetchone()
while row:
    print(row.sname)
    row = cursor.fetchone()

x='1'
y='1'
cursor.execute('''select sname,grade,cno
                  from s,sc 
                  where sc.sclass=? and sc.sno=? and sc.sno=s.sno and sc.sclass=s.sclass
                  ''',
               (x, y))
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()