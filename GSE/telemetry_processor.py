import config

# Handles telemetry processing
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
        # and put at the end of bd telemetry (pos 14)
        if len(data) > 17:
            for i in range(2):
                tmp = data.pop()
                data.insert(14, tmp)

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
            if value < self.packetMap[key]:
                data_dict[key] = (value, 0)
            else:
                data_dict[key] = (value, 1)

        return data_dict
