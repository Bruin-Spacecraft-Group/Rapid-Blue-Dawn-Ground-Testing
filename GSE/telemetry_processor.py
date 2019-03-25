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
        #potential TODO: convert values to numbers to process

        # if nff telemetry included, take umbilical data from back 
        # and put at the end of sc telemetry (pos 14)
        if len(data) > 20:
            for i in range(2):
                tmp = data.pop()
                data.insert(14, tmp)
        #check response type
        if data[0] == 'telemetry':
            #print("read telemetry")
            return self.processTelemetry(data[1:]), 'telemetry'
        elif data[0] == 'response':
            #print("\nread response")
            print("GOT HERE")
            return self.processCommandResponse(data[1:]), 'response'
        else:
            print("invalid packet, no response type")

    def processTelemetry(self, data):
        #convert flowmeter freq to flow rate
        if data[11] != "0":
            data[11] = float(data[11]) * 2.4/880 - 0.0009
            data[11] = str(data[11])

        data_dict = dict()
        #pair up names and data, checking limits 
        for key, value in zip(self.packetMap, data):
            value = float(value)
            #TODO: calibration step
            #check limits
            if value < self.packetMap[key][1] or value > self.packetMap[key][2]:
                data_dict[self.packetMap[key][0]] = (value, 1)
            else:
                data_dict[self.packetMap[key][0]] = (value, 0)
        return data_dict

    def processCommandResponse(self, data):
        return {
            "command": data[0],
            "voltage": data[1],
            'current': data[2],           
        }