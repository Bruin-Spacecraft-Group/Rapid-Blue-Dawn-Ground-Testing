import config

class TelemetryProcessor:
    """
    Sets calibration information and csv map (of the order of values in input list)
    """
    def __init__(self):
        self.umbilicalMap = config.UmbilicalMap
        self.scMap = config.ScMap
        self.nffMap = config.NffMap


    """
    Takes in a string of data in specific known order,
    outputs a dictionary in the form of {'name': [value, limit, limitstatus],.....}
    """
    def processPacket(self, packet):
        #splits csv data packet into list
        data = packet.split(',')
        
        ## filter between spacecraft and umbilical data packets
        if len(data) == 2 and data[0] != "response":
            return self.processTelemetry('ub', data), 'telemetry'
        else:
            #check response type
            if data[0] == 'telemetry':
                if len(data) < 20:
                    return self.processTelemetry('sc', data[1:]), 'telemetry'
                else:
                    return self.processTelemetry('sc_nff', data[1:]), 'telemetry'
            elif data[0] == 'response':
                print(data[1:])
                return self.processCommandResponse(data[1:]), 'response'
            else:
                print("invalid packet from spacecraft: no response type")
            
            
        

    def processTelemetry(self, telemType, data):
        data_dict = dict()
        if telemType == 'ub':
            for key, value in zip(self.umbilicalMap, data):
                if float(value) < self.umbilicalMap[key][0] or float(value) > self.umbilicalMap[key][1]:
                    # out of bounds
                    data_dict[key] = (value, 1)
                else:
                    # safe
                    data_dict[key] = (value, 0)  
        elif telemType == 'sc':
            for key, value in zip(self.scMap, data):
                #convert flowmeter freq to flow rate
                if key == 'flow_rate' and value != "0":
                    value = str(float(value) * 2.4/880 - 0.0009)
                
                if float(value) < self.scMap[key][0] or float(value) > self.scMap[key][1]:
                    # out of bounds
                    data_dict[key] = (value, 1)
                else:
                    # safe
                    data_dict[key] = (value, 0) 
        elif telemType == 'sc_nff':
            # first part is usual sc telementry
            for key, value in zip(self.scMap, data[:len(self.scMap)]):
                #convert flowmeter freq to flow rate
                if key == 'flow_rate' and value != "0":
                    value = str(float(value) * 2.4/880 - 0.0009)
                
                if float(value) < self.scMap[key][0] or float(value) > self.scMap[key][1]:
                    # out of bounds
                    data_dict[key] = (value, 1)
                else:
                    # safe
                    data_dict[key] = (value, 0)
            
            for key, value in zip(self.nffMap, data[len(self.scMap):]):
                if key == 'flight_state':
                    data_dict[key] = (value, 0)
                    continue

                if float(value) < self.nffMap[key][0] or float(value) > self.nffMap[key][1]:
                    # out of bounds
                    data_dict[key] = (value, 1)
                else:
                    # safe
                    data_dict[key] = (value, 0)   
        return data_dict
        
        #pair up names and data, checking limits 
        # for key, value in zip(self.packetMap, data):
        #     if key == 18:
        #         data_dict[self.packetMap[key][0]] = (value, 0) 
        #         continue
        #     value = float(value)
        #     #TODO: calibration step
        #     #check limits
        #     if value < self.packetMap[key][1] or value > self.packetMap[key][2]:
        #         # out of bounds
        #         data_dict[self.packetMap[key][0]] = (value, 1)
        #     else:
        #         # safe
        #         data_dict[self.packetMap[key][0]] = (value, 0)
        # return data_dict

    def processCommandResponse(self, data):
        return {
            "command": data[0]
            # "voltage": data[1],
            # 'current': data[2],           
        }