import csv
import glob

class TelemetryProcessor:
    
    #Global variable defining all data over time
    data_dict = []
    
    """
    Loads in any calibration files or csv map (of the order of values in input list)
    """
    def __init__(packetMap):
        #Selects csv file with unknown file name
        packet = glob.glob('*.csv')
        return packet
        
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
        #Reads csv and places into a dictionary
        with open(packet, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                row['Time_Start'],row['Flight State'],row['exp time'],row['Altitude'], \
                row['Velocity_X'],row['Velocity_Y'],row['Velocity_Z'],row['Attitude_X'],row['Attitude_Y'],row['Attitude_Z'], \
                row['Acceleration_X'],row['Acceleration_Y'],row['Acceleration_Z'],row['Ang_Vel_X'],row['Ang_Vel_Y'],row['Ang_Vel_Z'], \
                row['Liftoff Warning'],row['RCS Warning'],row['Escape Warning'],row['Chute Warning'],row['Landing Warning'],row['Fault Warning'], \
                row['Frequency Measure'],row['Magnetometer'],row['Current'],row['Voltage'],row['Timer'], \
                row['BD_Acceleration_X'],row['BD_Acceleration_Y'],row['BD_Acceleration_Z'], \
                row['BD_Ang_Vel_X'],row['BD_Ang_Vel_Y'],row['BD_Ang_Vel_Z'],row['MOSFET'],row['Time_End']
            #Note: Add Blue Dawn Errors to dictionary if they become part of csv
            '''
            Last 3 rows report Blue Dawn data. Order may need to be changed depending on final CSV data order. Written this
            way so that a list of dictionaries is created. Each dictionary represents all data at a given point in time
            '''
            #Question: How often is the CSV updated? This model assumes all data at a given time is reported in one row of the CSV
                data_dict.append(row)
                
            data_dict = addLimitStatus(data_dict)
            return data_dict
           
