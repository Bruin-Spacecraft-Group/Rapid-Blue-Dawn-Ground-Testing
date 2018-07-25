# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loginWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1056, 418)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setObjectName("label_title")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_title)
        spacerItem = QtWidgets.QSpacerItem(1017, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.formLayout.setItem(1, QtWidgets.QFormLayout.SpanningRole, spacerItem)
        self.label_blu = QtWidgets.QLabel(self.centralwidget)
        self.label_blu.setObjectName("label_blu")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_blu)
        self.lineEdit_blu = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_blu.setObjectName("lineEdit_blu")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEdit_blu)
        self.label_umb = QtWidgets.QLabel(self.centralwidget)
        self.label_umb.setObjectName("label_umb")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_umb)
        self.lineEdit_umb = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_umb.setObjectName("lineEdit_umb")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.lineEdit_umb)
        self.button_enter = QtWidgets.QPushButton(self.centralwidget)
        self.button_enter.setObjectName("button_enter")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.button_enter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1056, 39))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_title.setText(_translate("MainWindow", "Project Rapid - Blue Dawn Mission"))
        self.label_blu.setText(_translate("MainWindow", "Blue Dawn Port:"))
        self.label_umb.setText(_translate("MainWindow", "Umbilical Port:"))
        self.button_enter.setText(_translate("MainWindow", "Enter"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
