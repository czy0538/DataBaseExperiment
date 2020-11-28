# -*- coding: utf-8 -*-
import sys
import dataBase
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(670, 468)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(130, 50, 171, 41))
        self.label.setObjectName("label")
        self.answerDisplay = QtWidgets.QTextBrowser(Form)
        self.answerDisplay.setGeometry(QtCore.QRect(30, 100, 371, 281))
        self.answerDisplay.setObjectName("answerDisplay")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(450, 60, 141, 31))
        self.label_2.setObjectName("label_2")
        self.inputAdd = QtWidgets.QLineEdit(Form)
        self.inputAdd.setGeometry(QtCore.QRect(430, 100, 201, 71))
        self.inputAdd.setObjectName("inputAdd")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(450, 260, 161, 71))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(self.getMessage)  # 按钮槽函数，调用getmessage
        self.pushButton.clicked.connect(self.inputAdd.clear)  # 清空槽函数
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "180400501曹志远数据库实验3"))
        self.label.setText(_translate("Form", "结果显示列表"))
        self.label_2.setText(_translate("Form", "输入家庭地址"))
        self.pushButton.setText(_translate("Form", "查询"))

    # 获取查询结果
    def getMessage(self):
        message = self.inputAdd.text()  # 获取输入的字符串
        db = dataBase.DataBase()
        outputdata = ""  # 存放获得的内容
        cursor = db.cursor()  # 获取游标
        cursor.execute('''select sno,sname,ssex,sage,saddr
                              from s 
                              where s.saddr=?
                              ''',
                       (message))
        row = cursor.fetchone()  # 读取游标数据
        if row is None:  # 没有这个人输出没有
            outputdata = '查无此人'
        else:
            while row:
                for i in row:
                    outputdata = outputdata + i.strip() + ' '  # 去掉多余的空格
                outputdata = outputdata + '\n'
                row = cursor.fetchone()
        self.answerDisplay.setText(outputdata)  # 将数据发送到显示区域


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
