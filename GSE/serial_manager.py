import serial
import config
import sys
import zmq
from time import sleep
import argparse
from zmq import ZMQError
from PyQt5.Qt import QThread


class SerialManager(QThread):
    # initialize manager with ports to manage
    def __init__(self, sc_port, ub_port, server_addr, command_addr, nff_addr):
        QThread.__init__(self)
        # Try connecting to the ports first, and see if we can actually connect to the ports
        print("connecting to serial devices")
        try:
            self.sc = serial.Serial(
                port=sc_port,
                baudrate=config.BAUDRATE,
                timeout=config.TIMEOUT,
                write_timeout=config.TIMEOUT
            )
        except:
            print("ERROR: Cannot connect to Blue Dawn port at {}!".format(sc_port))
            sys.exit()

        try:
            self.ub = serial.Serial(
                port=ub_port,
                baudrate=config.BAUDRATE,
                timeout=config.TIMEOUT,
                write_timeout=config.TIMEOUT
            )
        except:
            print("ERROR: Cannot connect to Umbilical port at {}!".format(ub_port))
            sys.exit()

        print("opening serial manager zmq sockets")
        try:
            context = zmq.Context()
            self.server_socket = context.socket(zmq.PUB)
            self.server_socket.bind(server_addr)

            self.command_socket = context.socket(zmq.SUB)
            self.command_socket.connect(command_addr)
            self.command_socket.setsockopt_string(zmq.SUBSCRIBE, "")
            self.nff_socket = context.socket(zmq.SUB)
            self.nff_socket.connect(nff_addr)
            self.nff_socket.setsockopt_string(zmq.SUBSCRIBE, "")
        except:
            print("ERROR: Cannot connect to sockets!")
            sys.exit()
        print("serial manager initialized")


    # read a line of data from port
    # will block until newline recieved or timeout reached
    def readLine(self, ser):
        if ser.isOpen():
            packet = ser.readline()
            packet = packet.decode("utf-8")
            #print(packet)

            #remove carrige return and endline
            packet = packet.rstrip()
            
            return packet
        else:
            print("port not open")
            return None

    # send data to port
    # will block until finishes sending or timeout reached
    def writeToPort(self, ser, data):
        ser.write(data.encode("utf-8"))

    def manage(self):
        while True:
            try:
                command = self.command_socket.recv_string(flags=zmq.NOBLOCK)
                print("Sending command {}".format(command))
                self.writeToPort(self.sc, command)
            except ZMQError:
                pass
            sc_data=''
            ub_data=''
            while sc_data=='':
                sc_data = self.readLine(self.sc) 
            while ub_data=='': 
                ub_data = self.readLine(self.ub)
            packet = str(sc_data) + "," + str(ub_data)

            self.server_socket.send_string(packet)

    def run(self):
        self.Active = True
        while True:
            # check for commands/packets to send
            try:
                command = self.command_socket.recv_string(flags=zmq.NOBLOCK)
                #print("Sending command {}".format(command))
                self.writeToPort(self.sc, command)
            except ZMQError:
                pass
            try:
                nff_packet = self.nff_socket.recv_string(flags=zmq.NOBLOCK, encoding='ascii')
                #print("Sending nff packet {}".format(nff_packet))
                self.writeToPort(self.sc, nff_packet)
            except ZMQError:
                pass

            # read data
            sc_data=''
            ub_data=''
            while sc_data=='':
                sc_data = self.readLine(self.sc) 
            while ub_data=='': 
                ub_data = self.readLine(self.ub)
            packet = str(sc_data) + "," + str(ub_data)
            self.server_socket.send_string(packet)
    
    def stop(self):
        self.Active = False
        print("stopping serial manager")
        self.quit()


def main(args):
    """
    sc_port = input("Please enter Blue Dawn Port:")
    ub_port = input("Please enter Umbilical Port:")
    """
    """
    server_addr = input("Please enter Server Address:")
    command_addr = input("Please enter Commander Address:")
    """

    mySerialManager = SerialManager(args.sc_port, args.ub_port, \
        config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
    mySerialManager.manage()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send commands to flight computer')
    parser.add_argument('sc_port', help='a string specifying the command')
    parser.add_argument('ub_port', help='for commands which take additional arguments, e.g. timer')

    args = parser.parse_args()
    print(args)
    main(args)