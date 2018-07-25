import sys
import config
from PyQt5.QtWidgets import (QApplication, QAction, QMainWindow, QMenu, QInputDialog, QStatusBar)

from Ui_mainwindow import Ui_MainWindow 
from Ui_monitorWindow import Ui_Monitor

from serial_manager import SerialManager


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  

    def connectToSerialDevices(self):
        bd_port = "" #get addr
        ub_port = "" #get addr
        self.mySerialManager = SerialManager(bd_port, ub_port, config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
        self.mySerialManager.manage()
    


app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())