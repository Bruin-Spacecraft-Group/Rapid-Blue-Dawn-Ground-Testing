import sys
from PyQt5.QtWidgets import (QApplication, QAction, QMainWindow, QMenu, QInputDialog, QStatusBar)

from Ui_mainwindow import Ui_MainWindow 
from Ui_monitorWindow import Ui_Monitor 



#mainWindow.setupUi(QMainWindow)
"""
if __name__ == "__main__":
    mainWindow = Ui_MainWindow()
    monitorWindow = Ui_Monitor()

    mainWindow.setupUi(mainWindow)
"""
class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()  

app = QApplication(sys.argv)
w = AppWindow()
w.show()
sys.exit(app.exec_())