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
        #Upper limits for each parameter in the data
        limit = [1e7, 0, 1e7, 333000, 3500, 3500, 3500, 1000, 1000, 1000, 5, 5, 5, \
                  1000, 1000, 1000, 1, 1, 1, 1, 1, 1, 1000, 1000, 10000, 10000, 1e7, \
                  5, 5, 5, 1000, 1000, 1000, 0, 1e7]
        #In the case data file is empty
        if len(data.split(',')) == 0:
            pass
        else:
            count = 0
            for key, value in data.items():
                if count == 1 or count == 33:   #For 'Flight State' and 'MOSFET' Indices
                    pass
                elif float(value[0]) >= limit[count]:
                    count += 1
                    return value.append(' Limit Exceeded')
                elif float(value[0]) < limit[count]:
                    count += 1
                    return value.append(' Within Limit')
                else:
                    count += 1
                        
    """
    Takes in a list of data in specific known order,
    outputs a dictionary in the form of {'name': [value, limit, limitstatus],.....}
    """
    def processPacket(packet):
        #Reads data and places into a dictionary
        data = packet.split(',')
        data_dict = {'Time_Start':[data[0],1e7], 'Flight State':data[1], 'exp time':[data[2], 1e7], 'Altitude':[data[3],333000], \
            'Velocity_X':[data[4],3500], 'Velocity_Y':[data[5],3500], 'Velocity_Z':[data[6],3500], 'Attitude_X':[data[7],1000], \
            'Attitude_Y':[data[8],1000], 'Attitude_Z':[data[9],1000], 'Acceleration_X':[data[10],5], 'Acceleration_Y':[data[11],5], \
            'Acceleration_Z':[data[12],5], 'Ang_Vel_X':[data[13],1000], 'Ang_Vel_Y':[data[14],1000], 'Ang_Vel_Z':[data[15],1000], \
            'Liftoff Warning':[data[16],1], 'RCS Warning':[data[17],1], 'Escape Warning':[data[18],1], 'Chute Warning':[data[19],1], \
            'Landing Warning':[data[20],1], 'Fault Warning':[data[21],1], 'Frequency Measure':[data[22],1000], 'Magnetometer':[data[23],1000], \
            'Current':[data[24],10000], 'Voltage':[data[25],10000], 'Timer':[data[26],1e7] \
            'BD_Acceleration_X':[data[27],5], 'BD_Acceleration_Y' : [data[28],5], 'BD_Acceleration_Z':[data[29],5], \
            'BD_Ang_Vel_X':[data[30],1000], 'BD_Ang_Vel_Y':[data[31],1000], 'BD_Ang_Vel_Z':[data[32],1000], 'MOSFET':data[33], 'Time_End':[data[34],1e7]}
        #Note: Add Blue Dawn Errors to dictionary if they become part of data
        #Question: How often is the data updated? 
                
        data_dict = addLimitStatus(data_dict)
        return data_dict
           
