
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(866, 655)
        self.Do = QtWidgets.QPushButton(Form)
        self.Do.setGeometry(QtCore.QRect(560, 510, 181, 71))
        self.Do.setObjectName("Do")
        self.Display = QtWidgets.QLabel(Form)
        self.Display.setGeometry(QtCore.QRect(40, 70, 391, 201))
        self.Display.setObjectName("Display")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(560, 300, 125, 142))
        self.groupBox.setObjectName("groupBox")
        self.STable = QtWidgets.QCheckBox(self.groupBox)
        self.STable.setGeometry(QtCore.QRect(10, 30, 105, 22))
        self.STable.setObjectName("STable")
        self.SCTable = QtWidgets.QCheckBox(self.groupBox)
        self.SCTable.setGeometry(QtCore.QRect(10, 60, 105, 22))
        self.SCTable.setObjectName("SCTable")
        self.CTable = QtWidgets.QCheckBox(self.groupBox)
        self.CTable.setGeometry(QtCore.QRect(10, 90, 105, 22))
        self.CTable.setObjectName("CTable")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(560, 180, 231, 81))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(590, 130, 131, 31))
        self.label.setObjectName("label")
        self.UserInput = QtWidgets.QLineEdit(Form)
        self.UserInput.setGeometry(QtCore.QRect(30, 300, 401, 281))
        self.UserInput.setObjectName("UserInput")

        self.retranslateUi(Form)
        self.Do.clicked.connect(self.clicked_do)  # 按钮槽函数，执行查询

        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "180400501曹志远实验4"))
        self.Do.setText(_translate("Form", "执行"))
        self.Display.setText(_translate("Form", "180400501 曹志远"))
        self.groupBox.setTitle(_translate("Form", "表格选择"))
        self.STable.setText(_translate("Form", "S表"))
        self.SCTable.setText(_translate("Form", "SC表"))
        self.CTable.setText(_translate("Form", "C表"))
        self.comboBox.setItemText(0, _translate("Form", "插入"))
        self.comboBox.setItemText(1, _translate("Form", "修改"))
        self.comboBox.setItemText(2, _translate("Form", "查询"))
        self.comboBox.setItemText(3, _translate("Form", "删除"))
        self.label.setText(_translate("Form", "功能选择"))

    def clicked_do(self):
        """获取用户输入到UserInput，然后将输入区以及复选框清空"""
        self.InputMessage = self.UserInput.text()  # 获取输入内容
        self.Display.setText(self.InputMessage)
        self.getChecked()  # 获取选中的表
        self.clearChecked()  # 清空选中的表‘
        self.UserInput.clear()  # 清空输入区
        print(self.InputMessage)
        print(self.SelectedTable)

    def getChecked(self):
        """获取复选框内容，存储到元组SelectedTable中,0为S,1为SC，2为C"""
        self.SelectedTable = (self.STable.isChecked(), self.SCTable.isChecked(), self.CTable.isChecked())

    def clearChecked(self):
        """清空复选框"""
        self.STable.setCheckState(False)
        self.SCTable.setCheckState(False)
        self.CTable.setCheckState(False)


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())


main()
