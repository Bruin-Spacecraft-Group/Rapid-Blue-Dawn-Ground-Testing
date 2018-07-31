import config
class TelemetryProcessor:

"""
Sets calibration information and csv map (of the order of values in input list)
"""
def __init__(self, packetMap):
    self.packetMap = config.PACKETMAP

"""
Takes in a string of data in specific known order,
outputs a dictionary in the form of {'name': [value, limit, limitstatus],.....}
"""
def processPacket(self, packet):
    #splits csv data packet into list
    data = packet.split(',')

    #convert flowmeter freq to flow rate
    #data[22] = data[22] * 2.4/880 - 0.0009

    data_dict = dict()
    #pair up names and data, checking limits 
    for key, value in zip(self.packetMap, data):
        value = float(value)
        #TODO: calibration step

        #check limits
        if value < self.packetMap[key]:
            data_dict[key] = (value, 0)
        else:
            data_dict[key] = (value, 1)

    return data_dict