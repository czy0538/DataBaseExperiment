import sys
import pyodbc


class DataBase:
    # 数据库连接
    def __init__(self):
        server = 'SMALLBLACK\SQLEXPRESS'
        database = 'E3'# 数据库名字
        username = 'sa'
        password = '19991104'
        self.mycnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                       SERVER=' + server +
                              ';DATABASE=' + database +
                              ';UID=' + username +
                              ';PWD=' + password)

    # 游标获取
    def cursor(self):
        cursor = self.mycnxn.cursor()  # 游标
        return cursor


def main():
    db = DataBase()
    cursor = db.cursor()

    cursor.execute("SELECT * from s;")
    row = cursor.fetchone()
    while row:
        print(row.sname)
        row = cursor.fetchone()

    x = '1'
    y = '1'
    cursor.execute('''select sname,grade,cno
                      from s,sc 
                      where sc.sclass=? and sc.sno=? and sc.sno=s.sno and sc.sclass=s.sclass
                      ''',
                   (x, y))
    row = cursor.fetchone()
    while row:
        print(row)
        row = cursor.fetchone()


if __name__ == "__main__":
    # execute only if run as a script
    main()
