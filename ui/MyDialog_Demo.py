import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget
from shouye import Ui_Dialog
class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # 绑定按钮事件
        self.pushButton.clicked.connect(self.goto_cunhuo)
        self.pushButton_2.clicked.connect(self.goto_jinhuo)
        self.pushButton_3.clicked.connect(self.goto_xiaoshou)

    def goto_cunhuo(self):
        QtWidgets.QMessageBox.information(self, "提示", "跳转到存货界面")
        # 这里可以打开新窗口并关闭当前窗口

    def goto_jinhuo(self):
        QtWidgets.QMessageBox.information(self, "提示", "跳转到进货界面")

    def goto_xiaoshou(self):
        QtWidgets.QMessageBox.information(self, "提示", "跳转到销售界面")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dlg = MyDialog()
    dlg.show()
    sys.exit(app.exec())