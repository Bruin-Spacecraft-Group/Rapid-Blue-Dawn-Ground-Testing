import zmq
import datetime
import sys
import config 

class Commander():
    def __init__(self, input_addr, output_addr):
        context = zmq.Context()
        self.input_socket = context.socket(zmq.SUB)
        self.input_socket.connect(input_addr)
        self.input_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(output_addr)
    
    def command(self):
        """
        db.connect("testing")
        session = db.SESSIONMAKER()
        """
        while True:
            #read in list of commands and arguments from gui
            commandList = self.input_socket.recv_pyobj()
            
            #process commands

            #publish single command at a time to the serial manager
            for command in commands:
                self.output_socket.send_pyobj(command)

def main():
    """
    input_addr = input("Please enter the Serial Manager's publish address:")
    output_addr = input("Please enter the adress for the GUI to subscribe to:")
    """
    myCommander = Commander(config.COMMANDER_SUBSCRIBE, config.COMMANDER_PUBLISH)
    
    myCommander.command()

if __name__ == "__main__":
    main()
    