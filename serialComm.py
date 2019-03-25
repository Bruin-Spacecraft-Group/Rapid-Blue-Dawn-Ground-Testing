import serial
import sys
from time import sleep
import argparse

class SerialManager():
    # initialize manager with ports to manage
    def __init__(self, port):
        # Try connecting to the ports first, and see if we can actually connect to the ports
        try:
            self.serial = serial.Serial(
                port=port,
                baudrate=115200,
                timeout=1,
                write_timeout=1
            )
        except:
            print("ERROR: Cannot connect to Blue Dawn port at {}!".format(bd_port))
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

    def converse(self):
        command = input("Please enter command: ")
        self.writeToPort(self.serial, command)
        data = self.readLine(self.serial) 
        print(data)

def main(args):
    """
    bd_port = input("Please enter Blue Dawn Port:")
    ub_port = input("Please enter Umbilical Port:")
    """
    """
    server_addr = input("Please enter Server Address:")
    command_addr = input("Please enter Commander Address:")
    """

    mySerialManager = SerialManager(args.port)
    while True:
        mySerialManager.converse()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send commands to flight computer')
    parser.add_argument('port', help='what port is your device connected to?')

    args = parser.parse_args()
    print(args)
    main(args)