import zmq
import datetime
import sys
import config
#import database
from telemetry_processor import TelemetryProcessor

# A central server connecting multiple elements
# Gets data from serial, sends to gui, handles commander, etc.
class Server():
    def __init__(self, input_addr, output_addr, packet_map):
        context = zmq.Context()
        self.input_socket = context.socket(zmq.SUB)
        self.input_socket.connect(input_addr)
        self.input_socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(output_addr)

        self.processor = TelemetryProcessor(packet_map)

    def serve(self, textFile):
        print("server running...")

        while True:
            #read in raw packet from serial manager
            try:
                raw_packet = self.input_socket.recv_string()
                print("received string {}".format(raw_packet))

                processed_packet = self.processor.processPacket(raw_packet)

                #TODO: update this to a more useful form
                #save data to text file
                textFile.write("Timestamp: {},".format(datetime.datetime.now()))
                for key, value in processed_packet.items():
                    textFile.write("{}: {},".format(key, value))
                textFile.write("\n")
                textFile.flush()

                #publish processed packet data object to GUI
                self.output_socket.send_pyobj(processed_packet)
                print("sent obj")
            except Exception as e:
                print("error processing input, exception raised: {}".format(e))


def main():
    """
    input_addr = input("Please enter the Serial Manager's publish address:")
    output_addr = input("Please enter the adress for the GUI to subscribe to:")
    """
    packetMap = ["spacecraft_time", "flow_rate", "mosfet_state", "timer", "current", "voltage"]
    myServer = Server(config.SERVER_SUBSCRIBE, config.SERVER_PUBLISH, packetMap)

    date = str(datetime.datetime.now())
    FILENAME = 'Raw_Data/' + date
    FILENAME = FILENAME.replace(':', '_')
    txtfile = open(FILENAME, "w+")

    myServer.serve(txtfile)

if __name__ == "__main__":
    main()
