class TelemetryProcessor:
    
    """
    Loads in any calibration files or csv map (of the order of values in input list)
    """
    def __init__(packetMap):
        with open(packet) as data:
        return data
        
    """
    Adds limit status to each parameter in dictionary
    """
    def addLimitStatus(data):
        limits = [1e7, 0, 1e7, 333000, 3500, 3500, 3500, 1000, 1000, 1000, 5, 5, 5, \
                  1000, 1000, 1000, 1, 1, 1, 1, 1, 1, 100, 100, 10000, 10000, 1e7, \
                  5, 5, 5, 1000, 1000, 1000, 0, 1e7]
        if len(data) == 0:
            pass
        else:
            for dictionary in data:
                count = 0
                for key, value in dictionary.items():
                    if count == 1 or count == 33:   #For 'Flight State' Index
                        pass
                    elif float(value) >= limit[count]:
                        count += 1
                        return value + ', Limit Exceeded'
                    elif float(value) < limit[count]:
                        count += 1
                        return value + ', Within Limit'
                    else:
                        count += 1
                        pass
                        
    """
    Takes in a list of data in specific known order,
    outputs list of dict of the form [{("first_data_set", calibrated value), ....}, \
    {"second_data_set", calibrated value), ....}]
    """
    def processPacket(packet):
        #Reads data and places into a dictionary
        data = packet.split(',')
        data_dict = {'Time_Start' : data[0], 'Flight State' : data[1], 'exp time'] : data[2], 'Altitude' : data[3], \
            'Velocity_X' : data[4], 'Velocity_Y' : data[5], 'Velocity_Z' : data[6], 'Attitude_X' : data[7], \
            'Attitude_Y' : data[8], 'Attitude_Z' : data[9], 'Acceleration_X' : data[10], 'Acceleration_Y' : data[11], \
            'Acceleration_Z' : data[12], 'Ang_Vel_X' : data[13], 'Ang_Vel_Y' : data[14], 'Ang_Vel_Z' : data[15], \
            'Liftoff Warning' : data[16], 'RCS Warning' : data[17], 'Escape Warning' : data[18], 'Chute Warning' : data[19], \
            'Landing Warning' : data[20], 'Fault Warning' : data[21], 'Frequency Measure' : data[22], 'Magnetometer' : data[23], \
            'Current' : data[24], 'Voltage' : data[25], 'Timer' : data[26], \
            'BD_Acceleration_X' : data[27], 'BD_Acceleration_Y' : data[28], 'BD_Acceleration_Z' : data[29], \
            'BD_Ang_Vel_X' : data[30], 'BD_Ang_Vel_Y' : data[31], 'BD_Ang_Vel_Z' : data[32], 'MOSFET' : data[33], 'Time_End' : data[34]}
        #Note: Add Blue Dawn Errors to dictionary if they become part of csv
        #Question: How often is the data updated? 
                
        data_dict = addLimitStatus(data_dict)
        return data_dict
           
