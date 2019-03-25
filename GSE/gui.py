import sys
import zmq
import subprocess
import os
import serial.tools.list_ports

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

import config

from Ui_mainwindow import Ui_mainWindow 
from Ui_monitorWindow import Ui_Monitor

from serial_manager import SerialManager
from server import Server
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
        self.listSerialDevices()
        self.ui.buttonConnect.clicked.connect(self.openMonitor)

    def openMonitor(self):
        print("opening monitor")
        self.connectToSerialDevices()
        self.runServer()
        #self.socketThread = None
        self.monitor_window = QWidget()
        self.monitor_window.setStyleSheet(self.styleFile)
        self.monitor = Ui_Monitor()
        self.monitor.setupUi(self.monitor_window)
        self.monitor_window.show()
        self.console = ConsoleWidget()
        self.monitor.console.addWidget(self.console)
        self.openSockets()
        
    def runServer(self):
        self.server = Server(config.SERVER_SUBSCRIBE, config.SERVER_PUBLISH, config.packetMap)
        self.server.start()

    def listSerialDevices(self):
        comlist = serial.tools.list_ports.comports()
        for x in comlist:
            self.ui.sc_port.addItem(x.device)
            self.ui.ub_port.addItem(x.device)

    def connectToSerialDevices(self):
        sc_port = self.ui.sc_port.itemText(self.ui.sc_port.currentIndex())
        ub_port = self.ui.ub_port.itemText(self.ui.ub_port.currentIndex())
        self.serialManager = SerialManager(sc_port, ub_port, config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
        self.serialManager.start()
        #subprocess.Popen("python serial_manager.py {} {}".format(sc_port, ub_port), shell=True)
        
        #subprocess.Popen("{}/serial_manager.py {} {}".format(os.getcwd(), sc_port, ub_port), shell=True)
        #self.mySerialManager = SerialManager(sc_port, ub_port, config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
        #self.mySerialManager.manage()
    
    def openSockets(self):
        print("opening gui sockets")
        try:
            context = zmq.Context()
            self.telemSocket = context.socket(zmq.SUB)
            self.telemSocket.connect(config.GUI_SUBSCRIBE)
            self.telemSocket.setsockopt_string(zmq.SUBSCRIBE, '')
            
            self.commandSocket = context.socket(zmq.PUB)
            self.commandSocket.bind(config.GUI_PUBLISH)
            # print("sockets open")
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
        #print("\nReceived New Packet...")
        for key in msg:
            #print(key)
            #print(msg[key][0])
            if self.monitor.nff_groupbox.findChild(QLabel, key):
                item = self.monitor.nff_groupbox.findChild(QLabel, key)
            elif self.monitor.sc_groupbox.findChild(QLabel, key):
                item = self.monitor.sc_groupbox.findChild(QLabel, key)
            else:
                continue
            item.setText(str(msg[key][0]))
            if msg[key][1] == 1:
                item.setStyleSheet('color: #f93943') #red
            else:
                item.setStyleSheet('color: #063D23') #green


class SocketMonitor(QThread):
    signal = pyqtSignal(dict)
    def __init__(self,socket):
        QThread.__init__(self)
        self.socket = socket

    def run(self):
        print("Gui Socket Monitor Running")
        while True:
            msg = self.socket.recv_pyobj()
            #print(msg)
            if msg[0] == 'telemetry':
                #print("received telemetry")
                self.signal.emit(msg[1])
            elif msg[0] == 'response':
                #print("received response WOOO")
                self.signal.emit(msg[1])


if __name__ == '__main__':

    print("Running gui.py")
    app = QApplication(sys.argv)
    w = AppWindow()
    #w.openSockets()

    w.show()
    #w.connectToSerialDevices()

    sys.exit(app.exec_())