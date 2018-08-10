import serial
import config
import sys
import zmq
from time import sleep
import argparse
from zmq import ZMQError


class SerialManager():
    # initialize manager with ports to manage
    def __init__(self, bd_port, ub_port, server_addr, command_addr):
        # Try connecting to the ports first, and see if we can actually connect to the ports
        try:
            self.bd = serial.Serial(
                port=bd_port,
                baudrate=config.BAUDRATE,
                timeout=config.TIMEOUT,
                write_timeout=config.TIMEOUT
            )
        except:
            print("ERROR: Cannot connect to Blue Dawn port at {}!".format(bd_port))
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

        try:
            context = zmq.Context()
            self.server_socket = context.socket(zmq.PUB)
            self.server_socket.bind(server_addr)

            self.command_socket = context.socket(zmq.SUB)
            self.command_socket.connect(command_addr)
            self.command_socket.setsockopt_string(zmq.SUBSCRIBE, "")
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
            #packet = packet[2:len(packet)-5]
            
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
                self.writeToPort(self.bd, command)
            except ZMQError:
                pass
            bd_data=''
            ub_data=''
            while bd_data=='':
                bd_data = self.readLine(self.bd) 
            while ub_data=='': 
                ub_data = self.readLine(self.ub)
            packet = str(bd_data) + "," + str(ub_data)
            #print(packet)
            self.server_socket.send_string(packet)



def main(args):
    """
    bd_port = input("Please enter Blue Dawn Port:")
    ub_port = input("Please enter Umbilical Port:")
    """
    """
    server_addr = input("Please enter Server Address:")
    command_addr = input("Please enter Commander Address:")
    """

    mySerialManager = SerialManager(args.bd_port, args.ub_port, \
        config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
    mySerialManager.manage()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send commands to flight computer')
    parser.add_argument('bd_port', help='a string specifying the command')
    parser.add_argument('ub_port', help='for commands which take additional arguments, e.g. timer')

    args = parser.parse_args()
    print(args)
    main(args)