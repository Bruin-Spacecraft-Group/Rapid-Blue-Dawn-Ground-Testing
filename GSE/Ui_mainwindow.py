# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\andre\Documents\BruinSpace\Rapid\Rapid-Blue-Dawn-Ground-Testing\GSE\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(500, 220)
        mainWindow.setMinimumSize(QtCore.QSize(500, 0))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/MainLogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.port_groupbox = QtWidgets.QGroupBox(self.centralwidget)
        self.port_groupbox.setObjectName("port_groupbox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.port_groupbox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelBlue = QtWidgets.QLabel(self.port_groupbox)
        self.labelBlue.setMaximumSize(QtCore.QSize(16777215, 25))
        self.labelBlue.setObjectName("labelBlue")
        self.horizontalLayout.addWidget(self.labelBlue)
        self.bd_port = QtWidgets.QLineEdit(self.port_groupbox)
        self.bd_port.setInputMask("")
        self.bd_port.setText("")
        self.bd_port.setObjectName("bd_port")
        self.horizontalLayout.addWidget(self.bd_port)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelUmb = QtWidgets.QLabel(self.port_groupbox)
        self.labelUmb.setObjectName("labelUmb")
        self.horizontalLayout_3.addWidget(self.labelUmb)
        self.ub_port = QtWidgets.QLineEdit(self.port_groupbox)
        self.ub_port.setObjectName("ub_port")
        self.horizontalLayout_3.addWidget(self.ub_port)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.buttonConnect = QtWidgets.QPushButton(self.port_groupbox)
        self.buttonConnect.setDefault(False)
        self.buttonConnect.setFlat(False)
        self.buttonConnect.setObjectName("buttonConnect")
        self.verticalLayout_2.addWidget(self.buttonConnect)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.port_groupbox)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "Bruin Space GSE Setup"))
        self.title.setText(_translate("mainWindow", "Project Rapid - Blue Dawn"))
        self.port_groupbox.setTitle(_translate("mainWindow", "Setup"))
        self.labelBlue.setText(_translate("mainWindow", "Blue Dawn Port"))
        self.labelUmb.setText(_translate("mainWindow", "Umbilical Port"))
        self.buttonConnect.setText(_translate("mainWindow", "Connect"))

import resources_rc
