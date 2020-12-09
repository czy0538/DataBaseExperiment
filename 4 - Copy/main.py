import sys
from PyQt5.QtWidgets import QApplication
import GUI


def main():
    app = QApplication(sys.argv)
    # 初始化
    myWin = GUI.MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
