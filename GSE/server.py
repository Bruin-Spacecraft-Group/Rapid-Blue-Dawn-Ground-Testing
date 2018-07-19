import zmq
import datetime
import sys
import config
#import database
from telemetry_processor import TelemetryProcessor 

class Server():
    def __init__(self, input_addr, output_addr, packet_definitions):
        context = zmq.Context()
        self.input_socket = context.socket(zmq.SUB)
        self.input_socket.connect(input_addr)
        self.input_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(output_addr)

        self.processor = TelemetryProcessor(packet_definitions)
    
    def serve(self, textFile):
        """
        db.connect("testing")
        session = db.SESSIONMAKER()
        """
        while True:
            #read in raw packet from serial manager
            raw_packet = self.input_socket.recv_pyobj()
            processed_packet = self.processor.process(packet)
            
            #save data to text file
            textFile.write("Timestamp: {},".format(datetime.datetime.now()))
            for key, value in processed_packet.items():
                textFile.write("{}: {},".format(key, value))
            textFile.write("\n")
            textFile.flush()

            #publish processed packet data object to GUI
            self.output_socket.send_pyobj(processed_packet)

def main():
    """
    input_addr = input("Please enter the Serial Manager's publish address:")
    output_addr = input("Please enter the adress for the GUI to subscribe to:")
    """
    myServer = Server(config.SERVER_SUBSCRIBE, config.SERVER_PUBLISH)
    
    date = str(datetime.datetime.now())
    FILENAME = 'Raw_Data/' + date
    FILENAME = FILENAME.replace(':', '_')
    txtfile = open(FILENAME, "w")

    myServer.serve(txtfile)