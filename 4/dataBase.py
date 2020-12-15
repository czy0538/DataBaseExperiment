import sys
import pyodbc


class DataBase:
    # 数据库连接
    def __init__(self, messagebox=None):

        server = 'SMALLBLACK\SQLEXPRESS'
        database = 'ST'  # 数据库名字
        username = 'sa'
        password = '19991104'
        try:
            self.mycnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                       SERVER=' + server +
                                         ';DATABASE=' + database +
                                         ';UID=' + username +
                                         ';PWD=' + password)
        except pyodbc.Error as err:
            messagebox.MessageBox_Critical(err)
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
