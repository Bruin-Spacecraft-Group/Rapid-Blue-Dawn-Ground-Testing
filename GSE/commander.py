import zmq
import datetime
import sys
import config 
import argparse

"""class Commander():
    def __init__(self, input_addr, output_addr):
        context = zmq.Context()
        self.input_socket = context.socket(zmq.SUB)
        self.input_socket.connect(input_addr)
        self.input_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(output_addr)
    
    def command(self):
        ""
        db.connect("testing")
        session = db.SESSIONMAKER()
        "
        while True:
            #read in list of commands and arguments from gui
            commandList = self.input_socket.recv_pyobj()
            
            #process commands

            #publish single command at a time to the serial manager
            for command in commands:
                self.output_socket.send_pyobj(command)

def main():
    ""
    input_addr = input("Please enter the Serial Manager's publish address:")
    output_addr = input("Please enter the adress for the GUI to subscribe to:")
    "
    myCommander = Commander(config.COMMANDER_SUBSCRIBE, config.COMMANDER_PUBLISH)
    
    myCommander.command()

if __name__ == "__main__":
    main()
"""    
class Commander:
    def __init__(self):
        context = zmq.Context()
        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(config.COMMANDER_PUBLISH)
    
    def command(self):
        inputString = input("Please submit a command: ")
        args = inputString.split(" ")
        command = args[0]

        if command == "mosfet":
            if args[1] == "ENABLE":
                print("enabling electrodes")
                self.output_socket.send_string("cm1")
            else:
                print("disabling electrodes")
                self.output_socket.send_string("mosfet 0")
        elif command == "timer":
            if args[1] != None:
                print("setting timer for {} seconds".format(args[1]))
            else:
                print("please provide a timer duration")
        elif command == "reset":
            print("resetting")

if __name__ == '__main__':
    commander = Commander()
    commander.command()