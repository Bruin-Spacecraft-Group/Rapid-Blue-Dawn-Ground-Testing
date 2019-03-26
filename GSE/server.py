import zmq
import datetime
import sys
import config
#import database
from telemetry_processor import TelemetryProcessor 
from PyQt5.Qt import QThread

class Server(QThread):
    def __init__(self, parent_ui, input_addr, output_addr):
        QThread.__init__(self)
        self.ui = parent_ui
        
        context = zmq.Context()
        self.input_socket = context.socket(zmq.SUB)
        self.input_socket.connect(input_addr)
        self.input_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(output_addr)

        self.processor = TelemetryProcessor()
    
        # TODO: save data
        # date = str(datetime.datetime.now())
        # FILENAME = 'Raw_Data/' + date
        # FILENAME = FILENAME.replace(':', '_')
        # txtfile = open(FILENAME, "w+")

    def run(self):
        self.Active = True
        print("server running...")
        
        while True:
            #read in raw packet from serial manager
            try:
                raw_packet = self.input_socket.recv_string()
                # print("received string {}".format(raw_packet))

                processed_packet, packet_type = self.processor.processPacket(raw_packet)

                #TODO: update this to a more useful form
                #save data to text file
                # textFile.write("Timestamp: {},".format(datetime.datetime.now()))
                # for key, value in processed_packet[0].items():
                #     textFile.write("{}: {},".format(key, value))
                # textFile.write("\n")
                # textFile.flush()

                #publish processed packet data object to GUI
                self.output_socket.send_pyobj([packet_type, processed_packet])
                # print("sent obj\n")
            except Exception as e:
                print("error processing input, exception raised: {}".format(e))
    
    def stop(self):
        self.Active = False
        print("stopping server")
        self.quit()