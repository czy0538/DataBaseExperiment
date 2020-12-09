import sys
import pyodbc


class DataBase:
    # 数据库连接
    def __init__(self):
        server = 'SMALLBLACK\SQLEXPRESS'
        database = 'E3'  # 数据库名字
        username = 'sa'
        password = '19991104'
        self.mycnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                       SERVER=' + server +
                                     ';DATABASE=' + database +
                                     ';UID=' + username +
                                     ';PWD=' + password)
        self.cursor = self.mycnxn.cursor()  # 游标

    def getCursor(self):
        """游标获取"""
        return self.cursor

    def getCnxn(self):
        """连接管理"""
        return self.mycnxn

    def setValue(self, sqlString='', params=[]):
        """插入管理,sqlString负责传递sql语句，params是插入的列表"""
        try:
            self.cursor.executemany(sqlString, params)
        except pyodbc.DatabaseError as err:
            self.cnxn.rollback()
        else:
            self.cnxn.commit()


def main():
    db = DataBase()
    cursor = db.getCursor()
    # 数据库异常处理示例
    try:
        cursor.execute("SELECT * from Sc;")
        row = cursor.fetchone()
        while row:
            print(row.SNAME)
            row = cursor.fetchone()
    except pyodbc.DatabaseError as err:
        print(err)


if __name__ == "__main__":
    # execute only if run as a script
    main()
