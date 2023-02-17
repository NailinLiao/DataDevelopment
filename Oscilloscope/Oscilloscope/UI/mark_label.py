# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mark_label.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from PyQt5.QtCore import QCoreApplication
import json
from Config import *
import time


class Ui_MainWindow(QMainWindow):
    def __init__(self, json_path):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.comboBox.addItems(['条目1', '条目2', '条目3'])
        self.json_path = json_path
        if os.path.exists(self.json_path):
            f = open(self.json_path, 'r')  # 打开dict0.json
            self.json_data = json.load(f)
        else:
            self.json_data = json_struct
        file_name = str(os.path.split(json_path)[-1]).split('.')[0]
        self.json_data['video_name'] = file_name
        self.json_data['Modification_time'] = time.time()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(493, 98)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 113, 26))
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 40, 113, 26))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 40, 80, 26))
        self.pushButton.setObjectName("pushButton")
        # self.pushButton.clicked.connect(QCoreApplication.instance().quit)
        self.pushButton.clicked.connect(self.add_label)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(300, 40, 72, 26))
        self.comboBox.setObjectName("comboBox")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 100, 18))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(190, 10, 100, 18))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 10, 55, 20))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def write_label(self):
        with open(self.json_path, 'w') as f:
            # 将json数据写进一个文件当中去
            json.dump(self.json_data, f)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mark Label Tool"))
        self.pushButton.setText(_translate("MainWindow", "Push"))
        self.label.setText(_translate("MainWindow", "StartTime"))
        self.label_2.setText(_translate("MainWindow", "EndTime"))
        self.label_3.setText(_translate("MainWindow", "Label"))

        # 窗口关闭按钮事件

    def closeEvent(self, event):
        self.write_label()
        """Shuts down application on close."""
        reply = QMessageBox.question(self, '警告', '<font color=red><b>窗口关闭后，将终止本次运行</b></font>',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def add_label(self):
        start_time = self.lineEdit.text()
        end_time = self.lineEdit_2.text()
        label = self.comboBox.currentText()
        if len(start_time) < 5 or len(end_time) < 5:
            reply = QMessageBox.about(self, '提示', '输入有误')
        else:
            self.json_data['label'].append([label, start_time, end_time])
            reply = QMessageBox.about(self, '提示', '添加完成')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui_main = Ui_MainWindow('./a.json')
    ui_main.show()
    sys.exit(app.exec_())
