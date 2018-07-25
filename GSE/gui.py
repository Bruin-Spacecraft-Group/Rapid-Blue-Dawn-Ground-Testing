import sys
import zmq
import config
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

from Ui_mainwindow import Ui_mainWindow 
from Ui_monitorWindow import Ui_Monitor

from serial_manager import SerialManager


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
        self.socketThread = None
        self.monitor_window = QWidget()
        self.monitor_window.setStyleSheet(self.styleFile)
        self.monitor = Ui_Monitor()
        self.monitor.setupUi(self.monitor_window)
        self.monitor_window.show()
        self.openSockets()


    def connectToSerialDevices(self):
        bd_port = "" #get addr
        ub_port = "" #get addr
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
        print("\nReceived New Packet... \n{}".format(msg))
        for key in msg:
            self.monitor.bd_group_box.findChild(QLabel, key).setText(msg[key])

        """for item in msg['telem']:
            tid = item[0]
            val = item[1]
            print("tid: ", tid, "val: ", val)
            try:
                prev = self.slots[tid].time
            except KeyError:
                print("Slot does not exist. Making new slot...")
                prev = None
                self.slots[tid] = Slot(tid, 0, None)

            if self.slots[tid].time == None or curr > prev:
                print("new data... updating")
                self.slots[tid].value = val
                self.slots[tid].time = curr
                for plot in self.livePlots:
                    plot.update(tid,val,curr)
            else:
                print("old data (prev: ", prev, "curr: ", curr,")")"""

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