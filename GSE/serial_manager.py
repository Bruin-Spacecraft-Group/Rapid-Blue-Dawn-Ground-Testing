import serial
import config
import sys
import zmq
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
            packet = packet[2:len(packet)-5]
            
            return packet
        else:
            print("port {} not open".format(ser))  # TODO: this might not work
            return None

    # send data to port
    # will block until finishes sending or timeout reached
    def writeToPort(self, port, data):
        port.write(data)

    def manage(self):
        while True:
            try:
                command = self.command_socket.recv_string(flags=zmq.NOBLOCK)
                print("Sending command {}".format(command))
                self.writeToPort(self.bd, command)
            except ZMQError:
                pass

            bd_data = self.readLine(self.bd)
            #ub_data = self.readLine(self.ub)
            #packet = bd_data + "," + ub_data
            packet = bd_data
            print(packet)
            self.server_socket.send_pyobj(packet)


def main():
    bd_port = input("Please enter Blue Dawn Port:")
    ub_port = input("Please enter Umbilical Port:")

    """
    server_addr = input("Please enter Server Address:")
    command_addr = input("Please enter Commander Address:")
    """

    mySerialManager = SerialManager(
        bd_port, ub_port, config.SERIAL_PUBLISH, config.SERIAL_SUBSCRIBE)
    mySerialManager.manage()


if __name__ == "__main__":
    main()
