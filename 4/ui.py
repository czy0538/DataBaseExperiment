# -*- coding: utf-8 -*-
import sys

import pyodbc
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import dataBase


class Ui_Form(object):
    def __init__(self):
        self.table_item = ''
        db = dataBase.DataBase(messagebox=self)
        self.isSelected = [False] * 11  # 框选list,bool
        self.lineEditMessage = [''] * 11  # 获取所有文本框中的内容
        self.mode = ''  # 功能模式
        self.cursor = db.getCursor()
        self.cnxn = db.getCnxn()
        self.display_item = ''  # select子句
        self.condition_item = ''  # where子句
        self.table_item = ''  # from子句
        self.table_selected = [False] * 3  # 0为S,1为SC，2为C
        self.WrongInputError = False  # 输入错误为True

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(829, 644)
        self.lineEdit_display = QtWidgets.QTextEdit(Form)
        self.lineEdit_display.setGeometry(QtCore.QRect(20, 310, 781, 321))
        self.lineEdit_display.setObjectName("lineEdit_display")
        self.comboBox_mode = QtWidgets.QComboBox(Form)
        self.comboBox_mode.setGeometry(QtCore.QRect(190, 270, 261, 31))
        self.comboBox_mode.setObjectName("comboBox_mode")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.comboBox_mode.addItem("")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 270, 91, 31))
        self.label.setObjectName("label")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(110, 10, 579, 241))
        self.groupBox.setStyleSheet("selection-background-color: rgb(255, 255, 127);")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_sclass = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_sclass.setObjectName("checkBox_sclass")
        self.gridLayout.addWidget(self.checkBox_sclass, 0, 0, 1, 1)
        self.lineEdit_sclass = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_sclass.setObjectName("lineEdit_sclass")
        self.gridLayout.addWidget(self.lineEdit_sclass, 0, 1, 1, 1)
        self.checkBox_cno = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_cno.setObjectName("checkBox_cno")
        self.gridLayout.addWidget(self.checkBox_cno, 0, 2, 1, 1)
        self.lineEdit_cno = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cno.setObjectName("lineEdit_cno")
        self.gridLayout.addWidget(self.lineEdit_cno, 0, 3, 1, 1)
        self.checkBox_sno = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_sno.setObjectName("checkBox_sno")
        self.gridLayout.addWidget(self.checkBox_sno, 1, 0, 1, 1)
        self.lineEdit_sno = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_sno.setObjectName("lineEdit_sno")
        self.gridLayout.addWidget(self.lineEdit_sno, 1, 1, 1, 1)
        self.checkBox_cname = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_cname.setObjectName("checkBox_cname")
        self.gridLayout.addWidget(self.checkBox_cname, 1, 2, 1, 1)
        self.lineEdit_cname = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cname.setObjectName("lineEdit_cname")
        self.gridLayout.addWidget(self.lineEdit_cname, 1, 3, 1, 1)
        self.checkBox_sname = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_sname.setObjectName("checkBox_sname")
        self.gridLayout.addWidget(self.checkBox_sname, 2, 0, 1, 1)
        self.lineEdit_sname = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_sname.setObjectName("lineEdit_sname")
        self.gridLayout.addWidget(self.lineEdit_sname, 2, 1, 1, 1)
        self.checkBox_cpno = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_cpno.setObjectName("checkBox_cpno")
        self.gridLayout.addWidget(self.checkBox_cpno, 2, 2, 1, 1)
        self.lineEdit_cpno = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cpno.setObjectName("lineEdit_cpno")
        self.gridLayout.addWidget(self.lineEdit_cpno, 2, 3, 1, 1)
        self.checkBox_ssex = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ssex.setObjectName("checkBox_ssex")
        self.gridLayout.addWidget(self.checkBox_ssex, 3, 0, 1, 1)
        self.lineEdit_ssex = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_ssex.setObjectName("lineEdit_ssex")
        self.gridLayout.addWidget(self.lineEdit_ssex, 3, 1, 1, 1)
        self.checkBox_ccredit = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_ccredit.setObjectName("checkBox_ccredit")
        self.gridLayout.addWidget(self.checkBox_ccredit, 3, 2, 1, 1)
        self.lineEdit_ccredit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_ccredit.setObjectName("lineEdit_ccredit")
        self.gridLayout.addWidget(self.lineEdit_ccredit, 3, 3, 1, 1)
        self.checkBox_sage = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_sage.setObjectName("checkBox_sage")
        self.gridLayout.addWidget(self.checkBox_sage, 4, 0, 1, 1)
        self.lineEdit_sage = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_sage.setText("")
        self.lineEdit_sage.setObjectName("lineEdit_sage")
        self.gridLayout.addWidget(self.lineEdit_sage, 4, 1, 1, 1)
        self.checkBox_grade = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_grade.setObjectName("checkBox_grade")
        self.gridLayout.addWidget(self.checkBox_grade, 4, 2, 1, 1)
        self.lineEdit_grade = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_grade.setObjectName("lineEdit_grade")
        self.gridLayout.addWidget(self.lineEdit_grade, 4, 3, 1, 1)
        self.checkBox_sdept = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_sdept.setObjectName("checkBox_sdept")
        self.gridLayout.addWidget(self.checkBox_sdept, 5, 0, 1, 1)
        self.lineEdit_sdept = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_sdept.setObjectName("lineEdit_sdept")
        self.gridLayout.addWidget(self.lineEdit_sdept, 5, 1, 1, 1)
        self.pushButton_ok = QtWidgets.QPushButton(Form)
        self.pushButton_ok.setGeometry(QtCore.QRect(470, 270, 112, 34))
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.pushButton_clear = QtWidgets.QPushButton(Form)
        self.pushButton_clear.setGeometry(QtCore.QRect(590, 270, 112, 34))
        self.pushButton_clear.setObjectName("pushButton_clear")

        # 信号
        # 选中确定按钮后获取选中的值随后清空所有输入内容
        self.pushButton_ok.clicked.connect(self.PushButton_ok)
        # 选中清空按钮后清空文本框和所有输入内容
        self.pushButton_clear.clicked.connect(self.clearLineEdit)
        self.pushButton_clear.clicked.connect(self.clearCheckBox)
        self.pushButton_clear.clicked.connect(self.lineEdit_display.clear)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "180400501 曹志远 数据库实验4"))
        self.lineEdit_display.setPlainText(_translate("Form", "                                   180400501 曹志远"))
        self.comboBox_mode.setItemText(0, _translate("Form", "查询"))
        self.comboBox_mode.setItemText(1, _translate("Form", "插入"))
        self.comboBox_mode.setItemText(2, _translate("Form", "删除"))
        self.comboBox_mode.setItemText(3, _translate("Form", "修改"))
        self.label.setText(_translate("Form", "功能选择"))
        self.groupBox.setTitle(_translate("Form", "项目选择区"))
        self.checkBox_sclass.setText(_translate("Form", "班级"))
        self.checkBox_cno.setText(_translate("Form", "课程号"))
        self.checkBox_sno.setText(_translate("Form", "学号"))
        self.checkBox_cname.setText(_translate("Form", "课程名"))
        self.checkBox_sname.setText(_translate("Form", "姓名"))
        self.checkBox_cpno.setText(_translate("Form", "先修课"))
        self.checkBox_ssex.setText(_translate("Form", "性别"))
        self.checkBox_ccredit.setText(_translate("Form", "学分"))
        self.checkBox_sage.setText(_translate("Form", "年龄"))
        self.checkBox_grade.setText(_translate("Form", "成绩"))
        self.checkBox_sdept.setText(_translate("Form", "系"))
        self.pushButton_ok.setText(_translate("Form", "确定"))
        self.pushButton_clear.setText(_translate("Form", "清空"))

    def getSelected(self):
        """检测每个框是否被选中"""
        self.isSelected = [False] * 11
        self.isSelected[0] = self.checkBox_sclass.isChecked()
        self.isSelected[1] = self.checkBox_sno.isChecked()
        self.isSelected[2] = self.checkBox_sname.isChecked()
        self.isSelected[3] = self.checkBox_ssex.isChecked()
        self.isSelected[4] = self.checkBox_sage.isChecked()
        self.isSelected[5] = self.checkBox_sdept.isChecked()
        self.isSelected[6] = self.checkBox_cno.isChecked()
        self.isSelected[7] = self.checkBox_cname.isChecked()
        self.isSelected[8] = self.checkBox_cpno.isChecked()
        self.isSelected[9] = self.checkBox_ccredit.isChecked()
        self.isSelected[10] = self.checkBox_grade.isChecked()

    def clearCheckBox(self):
        """清空所有的选择框"""
        self.checkBox_sclass.setCheckState(False)
        self.checkBox_sno.setCheckState(False)
        self.checkBox_sname.setCheckState(False)
        self.checkBox_ssex.setCheckState(False)
        self.checkBox_sage.setCheckState(False)
        self.checkBox_sdept.setCheckState(False)
        self.checkBox_cno.setCheckState(False)
        self.checkBox_cname.setCheckState(False)
        self.checkBox_cpno.setCheckState(False)
        self.checkBox_ccredit.setCheckState(False)
        self.checkBox_grade.setCheckState(False)

    def clearLineEdit(self):
        """清空所有的lineEdit"""
        self.lineEdit_sname.clear()
        self.lineEdit_sno.clear()
        self.lineEdit_sage.clear()
        self.lineEdit_ssex.clear()
        self.lineEdit_sdept.clear()
        self.lineEdit_cpno.clear()
        self.lineEdit_cno.clear()
        self.lineEdit_ccredit.clear()
        self.lineEdit_cname.clear()
        self.lineEdit_sclass.clear()
        self.lineEdit_grade.clear()

    def getLineEdit(self):
        """获取选中的框中值"""
        self.lineEditMessage = [''] * 11
        self.lineEditMessage[0] = self.lineEdit_sclass.text()
        self.lineEditMessage[1] = self.lineEdit_sno.text()
        self.lineEditMessage[2] = self.lineEdit_sname.text()
        self.lineEditMessage[3] = self.lineEdit_ssex.text()
        self.lineEditMessage[4] = self.lineEdit_sage.text()
        self.lineEditMessage[5] = self.lineEdit_sdept.text()
        self.lineEditMessage[6] = self.lineEdit_cno.text()
        self.lineEditMessage[7] = self.lineEdit_cname.text()
        self.lineEditMessage[8] = self.lineEdit_cpno.text()
        self.lineEditMessage[9] = self.lineEdit_ccredit.text()
        self.lineEditMessage[10] = self.lineEdit_grade.text()
        print(self.lineEditMessage)

    def MessageBox_Critical(self, err):
        """严重错误"""
        QMessageBox.critical(self, '错误', str(err),
                             QMessageBox.Abort, QMessageBox.Abort)
        sys.exit(-1)

    def MessageBox_wrongInput(self, message='输入条件有误，请重新输入'):
        """输入错误弹出该框"""
        QMessageBox.warning(self, '输入错误', message, QMessageBox.Ok)
        # 执行清理
        raise ValueError('输入错误！')

    def PushButton_ok(self):
        """按下ok按钮后的行为"""
        # 获取和清空
        try:

            # 获取模式,基本输入框信息
            self.mode = self.comboBox_mode.currentText()
            self.getSelected()
            self.getLineEdit()
            display = ''
            if self.mode == '查询':
                self.getTable_selected()
                self.getTable_item()
                self.getCondition_item()
                self.getDisplay_item()
                if len(self.condition_item) != 0:
                    mysql = 'select distinct' + self.display_item + ' from' + self.table_item + \
                            ' where' + self.condition_item + ';'
                else:
                    mysql = 'select distinct' + self.display_item + ' from' + self.table_item + ';'
                for row in self.cursor.execute(mysql):
                    print(row.cursor_description)  # 行描述信息
                    for i in row:
                        display += str(i).strip().ljust(10, ' ')
                    display += '\n'
            elif self.mode == '修改':
                self.getTable_selected()
                self.getCondition_item()
                self.isSingleTable()  # 检测单表
                self.getTable_item()
                mysql = 'update ' + self.table_item + ' set ' + self.lineEdit_display.toPlainText() \
                        + ' where ' + self.condition_item
                self.lineEdit_display.clear()
                updated = self.cursor.execute(mysql).rowcount
                display = str(updated) + '行被修改'
                self.cnxn.commit()
            elif self.mode == '删除':
                self.getTable_selected()
                self.isSingleTable()  # 检测from合法性
                self.getTable_item()  # FROM子句
                self.getCondition_item()
                mysql = 'delete from ' + self.table_item + ' where ' + self.condition_item
                deleted = self.cursor.execute(mysql).rowcount
                display = str(deleted) + '行被删除'
                self.cnxn.commit()

            elif self.mode == '插入':
                self.getTable_selected()
                self.isSingleTable()  # 检测单表
                self.getTable_item()
                insert_values = ''
                # S表插入
                if self.table_selected[0]:
                    self.table_item = ' S '
                    for i in self.lineEditMessage[0:6]:
                        if len(i) == 0:
                            insert_values += '\'NULL\','
                        else:
                            insert_values += '\'%s\',' % i  # 字符拼接
                # sc表插入
                elif self.table_selected[1]:
                    self.table_item = ' SC '
                    temp = self.lineEditMessage[0:2] + list(self.lineEditMessage[6])
                    for i in temp:
                        if len(i) == 0:
                            insert_values += '\'NULL\','
                        else:
                            insert_values += '\'%s\',' % i  # 字符拼接
                    if len(self.lineEditMessage[10]) != 0:
                        insert_values += '%s,' % self.lineEditMessage[10]
                    else:
                        insert_values += '%s,' % '-1'
                # C表插入
                elif self.table_selected[2]:
                    self.table_item = ' C '
                    for i in self.lineEditMessage[6:9]:
                        if len(i) == 0:
                            insert_values += '\'NULL\','
                        else:
                            insert_values += '\'%s\',' % i  # 字符拼接
                    if len(self.lineEditMessage[9]) != 0:
                        insert_values += '%s,' % self.lineEditMessage[9]
                    else:
                        insert_values += '%s,' % '-1'

                insert_values = insert_values[0:len(insert_values) - 1]
                mysql = 'insert into ' + self.table_item + ' values (' + insert_values + ' );'
                print(mysql)
                inserted = self.cursor.execute(mysql).rowcount
                display = str(inserted) + '行被插入'
                self.cnxn.commit()
        except ValueError:
            self.clearCheckBox()
            self.clearLineEdit()
        except pyodbc.Error as err:
            self.clearCheckBox()
            self.clearLineEdit()
            self.cnxn.rollback()
            display = str(err)
        else:
            # 执行清理
            self.clearCheckBox()
            self.clearLineEdit()
            self.lineEdit_display.clear()
        finally:
            if len(display) == 0:
                display = '没有数据'
            self.lineEdit_display.setPlainText(display)

    def getDisplay_item(self):
        """获取select子句内容"""
        self.display_item = ' '
        # sclass
        if self.isSelected[0] and len(self.lineEditMessage[0]) == 0:
            if self.table_selected[0]:
                self.display_item += 'S.sclass,'
            else:
                self.display_item += 'SC.sclass,'
        # sno
        if self.isSelected[1] and len(self.lineEditMessage[1]) == 0:
            if self.table_selected[0]:
                self.display_item += 'S.sno,'
            else:
                self.display_item += 'SC.sno,'

        # cno
        if self.isSelected[6] and len(self.lineEditMessage[6]) == 0:
            if self.table_selected[2]:
                self.display_item += 'C.cno,'
            else:
                self.display_item += 'SC.cno,'

        if self.isSelected[2] and len(self.lineEditMessage[2]) == 0:
            self.display_item += 'sname,'

        if self.isSelected[3] and len(self.lineEditMessage[3]) == 0:
            self.display_item += 'ssex,'

        if self.isSelected[4] and len(self.lineEditMessage[4]) == 0:
            self.display_item += 'sage,'

        if self.isSelected[5] and len(self.lineEditMessage[5]) == 0:
            self.display_item += 'sdept,'

        if self.isSelected[7] and len(self.lineEditMessage[7]) == 0:
            self.display_item += 'cname,'

        if self.isSelected[8] and len(self.lineEditMessage[8]) == 0:
            self.display_item += 'cpno,'

        if self.isSelected[9] and len(self.lineEditMessage[9]) == 0:
            self.display_item += 'ccredit,'

        if self.isSelected[10] and len(self.lineEditMessage[10]) == 0:
            self.display_item += 'grade,'

        self.display_item = self.display_item[0: len(self.display_item) - 1]  # 去掉结尾的逗号
        if len(self.display_item) == 0:
            self.MessageBox_wrongInput()

    def getCondition_item(self):
        """获取where子句内容"""
        self.condition_item = ' '
        # 表连接：
        if self.table_selected[0] and self.table_selected[1] and not self.table_selected[2]:  # S,SC
            self.condition_item += 'S.sclass=SC.sclass and S.sno=SC.sno and '
        elif not self.table_selected[0] and self.table_selected[1] and self.table_selected[2]:  # SC,C
            self.condition_item += 'C.cno=SC.cno and '
        elif self.table_selected[0] and self.table_selected[1] and self.table_selected[2]:  # 全选
            self.condition_item += 'S.sclass=SC.sclass and S.sno=SC.sno and SC.cno=C.cno and '
            # 其他情况无需表连接
            # 其他where子句
            # sclass
        if self.isSelected[0] and len(self.lineEditMessage[0]) != 0:
            if self.table_selected[0]:
                self.condition_item += 'S.sclass=' + self.lineEditMessage[0] + ' and '
            else:
                self.condition_item += 'SC.sclass=' + self.lineEditMessage[0] + ' and '
            # sno
        if self.isSelected[1] and len(self.lineEditMessage[1]) != 0:
            if self.table_selected[0]:
                self.condition_item += 'S.sno=' + self.lineEditMessage[1] + ' and '
            else:
                self.condition_item += 'SC.sno=' + self.lineEditMessage[1] + ' and '

            # cno
        if self.isSelected[6] and len(self.lineEditMessage[6]) != 0:
            if self.table_selected[2]:
                self.condition_item += 'C.cno=' + self.lineEditMessage[6] + ' and '
            else:
                self.condition_item += 'SC.cno=' + self.lineEditMessage[6] + ' and '

        if self.isSelected[2] and len(self.lineEditMessage[2]) != 0:
            self.condition_item += 'sname=' + self.lineEditMessage[2] + ' and '

        if self.isSelected[3] and len(self.lineEditMessage[3]) != 0:
            self.condition_item += 'ssex=' + self.lineEditMessage[3] + ' and '

        if self.isSelected[4] and len(self.lineEditMessage[4]) != 0:
            self.condition_item += 'sage=' + self.lineEditMessage[4] + ' and '

        if self.isSelected[5] and len(self.lineEditMessage[5]) != 0:
            self.condition_item += 'sdept=' + self.lineEditMessage[5] + ' and '

        if self.isSelected[7] and len(self.lineEditMessage[7]) != 0:
            self.condition_item += 'cname=' + self.lineEditMessage[7] + ' and '

        if self.isSelected[8] and len(self.lineEditMessage[8]) != 0:
            self.condition_item += 'cpno=' + self.lineEditMessage[8] + ' and '

        if self.isSelected[9] and len(self.lineEditMessage[9]) != 0:
            self.condition_item += 'ccredit=' + self.lineEditMessage[9] + ' and '

        if self.isSelected[10] and len(self.lineEditMessage[10]) != 0:
            self.condition_item += 'grade=' + self.lineEditMessage[10] + ' and '

        self.condition_item = self.condition_item[0:len(self.condition_item) - 4]
        print(self.condition_item)

    def getTable_item(self):
        """获取from子句内容"""
        self.table_item = ' SC,'
        # 默认选中SC表以支撑对三个键的选中
        if self.table_selected[0]:
            self.table_item = ' S,'
        if self.table_selected[1]:  # 选中成绩一定需要SC表
            self.table_item += ' SC,'
        if self.table_selected[2]:
            self.table_item += ' C,'
        self.table_item = self.table_item[0:len(self.table_item) - 1]
        print(self.table_item)

    def getTable_selected(self):
        """获取表是否选中"""
        self.table_selected = [False] * 3
        if self.isSelected[10]:  # SC选中检测
            self.table_selected[1] = True
        for i in range(7, 10):  # C选中检测
            if self.isSelected[i]:
                self.table_selected[2] = True
        for i in range(2, 6):
            if self.isSelected[i]:  # S选中检测
                self.table_selected[0] = True
        # 如果没有表被选中，则输出error
        # 选中S,C但没选中SC也为逻辑错误
        i = 0
        while i < 3:
            if self.table_selected[i]:
                break
            i += 1
        if i == 3 or (self.table_selected[0] and self.table_selected[2] and not self.table_selected[1]):
            self.MessageBox_wrongInput()

    def isSingleTable(self):
        """返回选中表是否只为一个,不为一个引起异常"""
        count = 0
        for i in self.table_selected:
            if i:
                count += 1
        if count != 1:
            self.MessageBox_wrongInput()


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)
