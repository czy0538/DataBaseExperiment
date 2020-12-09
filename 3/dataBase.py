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
        self.mycursor = self.mycnxn.cursor() # 游标

    def getCursor(self):
        """游标获取"""
        return self.mycursor
