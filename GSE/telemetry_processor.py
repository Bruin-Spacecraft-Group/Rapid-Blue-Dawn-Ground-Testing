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
        limits = []
        if len(data) == 0:
            pass
        else:
            for dictionary in data:
                count = 0
                for key, value in dictionary.items():
                    if value >= limit[count]:
                        count += 1
                        return value + ', Limit Exceeded'
                    elif value < limit[count]:
                        count += 1
                        return value + ', Within Limit'
                    else:
                        count += 1
                        return value + ', Error'
                        
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
                
                data_dict.append(row)
            #Note: Add Blue Dawn Errors to dictionary if they end up in CSV
            '''
            Last 3 rows report Blue Dawn data. Order may need to be changed depending on final CSV data order. Written this
            way so that a list of dictionaries is created. Each dictionary represents all data at a given point in time
            '''
            #Question: How often is the CSV updated? This model assumes all data at a given time is reported in one row of the CSV
            return data_dict
            

            
            
