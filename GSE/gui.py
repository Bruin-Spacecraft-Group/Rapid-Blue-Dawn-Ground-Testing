import sys
import zmq
import config
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

from Ui_mainwindow import Ui_mainWindow 
from Ui_monitorWindow import Ui_Monitor

from serial_manager import SerialManager
from console import ConsoleWidget


class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainWindow()
        self.styleFile = open( "styles.qss" ).read()
        self.setStyleSheet(self.styleFile)
        self.ui.setupUi(self)
        self.socketThread = None
        #self.show()
        self.ui.buttonConnect.clicked.connect(self.openMonitor)

    def openMonitor(self):
        print("opening")
        self.connectToSerialDevices()
        #self.socketThread = None
        self.monitor_window = QWidget()
        self.monitor_window.setStyleSheet(self.styleFile)
        self.monitor = Ui_Monitor()
        self.monitor.setupUi(self.monitor_window)
        self.monitor_window.show()
        self.console = ConsoleWidget()
        self.monitor.console.addWidget(self.console)
        self.openSockets()


    def connectToSerialDevices(self):
        print("connecting to serial devices")
        bd_port = self.ui.bd_port.text()
        ub_port = self.ui.ub_port.text()
        self.mySerialManager = SerialManager(bd_port, ub_port, config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
        self.mySerialManager.manage()
    
    def openSockets(self):
        print("opening sockets")
        try:
            context = zmq.Context()
            self.telemSocket = context.socket(zmq.SUB)
            self.telemSocket.connect(config.GUI_SUBSCRIBE)
            self.telemSocket.setsockopt_string(zmq.SUBSCRIBE, '')
            
            self.commandSocket = context.socket(zmq.PUB)
            self.commandSocket.bind(config.GUI_PUBLISH)
            print("sockets open")
        except (zmq.ZMQError, zmq.ZMQBindError) as err:
            print("Error: {}".format(err))
            return
        
        if(self.socketThread is not None):
            self.socketThread.terminate()
            self.socketThread.socket.close()

        self.socketThread = SocketMonitor(self.telemSocket)
        self.socketThread.signal.connect(self.gotSig)
        self.socketThread.start()

    def gotSig(self, msg):
        print("\nReceived New Packet...")
        for key in msg:
            #print(key)
            #print(msg[key][0])
            if self.monitor.nff_groupbox.findChild(QLabel, key):
                self.monitor.nff_groupbox.findChild(QLabel, key).setText(str(msg[key][0]))
            elif self.monitor.bd_groupbox.findChild(QLabel, key):
                self.monitor.bd_groupbox.findChild(QLabel, key).setText(str(msg[key][0]))

class SocketMonitor(QThread):
    signal = pyqtSignal(dict)
    def __init__(self,socket):
        QThread.__init__(self)
        self.socket = socket

    def run(self):
        print("running")
        while True:
            msg = self.socket.recv_pyobj()
            print(msg)
            self.signal.emit(msg)

app = QApplication(sys.argv)
w = AppWindow()
#w.openSockets()

w.show()
#w.connectToSerialDevices()

sys.exit(app.exec_())