# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from Ui_monitorWindow import Ui_Monitor

class Ui_mainWindow(object):
    def openWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Monitor();
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, loginWindow):
        loginWindow.setObjectName("loginWindow")
        loginWindow.resize(706, 320)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(loginWindow.sizePolicy().hasHeightForWidth())
        loginWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/MainLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        loginWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(loginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 661, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.groupBox = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.groupBox.setObjectName("groupBox")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupBox)
        self.formLayoutWidget.setGeometry(QtCore.QRect(9, 19, 661, 211))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.labelBlue = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelBlue.setObjectName("labelBlue")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelBlue)
        self.lineEditBlue = QtWidgets.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditBlue.sizePolicy().hasHeightForWidth())
        self.lineEditBlue.setSizePolicy(sizePolicy)
        self.lineEditBlue.setInputMask("")
        self.lineEditBlue.setText("")
        self.lineEditBlue.setObjectName("lineEditBlue")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEditBlue)
        self.labelUmb = QtWidgets.QLabel(self.formLayoutWidget)
        self.labelUmb.setObjectName("labelUmb")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelUmb)
        self.lineEditUmb = QtWidgets.QLineEdit(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEditUmb.sizePolicy().hasHeightForWidth())
        self.lineEditUmb.setSizePolicy(sizePolicy)
        self.lineEditUmb.setObjectName("lineEditUmb")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditUmb)
        self.buttonConnect = QtWidgets.QPushButton(self.formLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonConnect.sizePolicy().hasHeightForWidth())
        self.buttonConnect.setSizePolicy(sizePolicy)
        self.buttonConnect.setObjectName("buttonConnect")
        self.buttonConnect.clicked.connect(self.openWindow)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.buttonConnect)
        self.verticalLayout.addWidget(self.groupBox)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 8)
        loginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(loginWindow)
        self.statusbar.setObjectName("statusbar")
        loginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(loginWindow)
        QtCore.QMetaObject.connectSlotsByName(loginWindow)

    def retranslateUi(self, loginWindow):
        _translate = QtCore.QCoreApplication.translate
        loginWindow.setWindowTitle(_translate("loginWindow", "Bruin Space GSE Setup"))
        self.label.setText(_translate("loginWindow", "Project Rapid - Blue Dawn"))
        self.groupBox.setTitle(_translate("loginWindow", "Setup"))
        self.labelBlue.setText(_translate("loginWindow", "Blue Dawn Port"))
        self.labelUmb.setText(_translate("loginWindow", "Umbilical Port"))
        self.buttonConnect.setText(_translate("loginWindow", "Connect"))

import resources_rc
