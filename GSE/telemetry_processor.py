import csv
import glob

class TelemetryProcessor:
    """
    Loads in any calibration files or csv map (of the order of values in input list)
    """
    def __init__(packetMap):
        #Selects csv file with unknown file name
        data = glob.glob('*.csv')
        return data
            
    """
    Takes in a list of data in specific known order,
    outputs dict of the form ["name", calibrated value, limit status)]
    """
    def processPacket(packet):
        #Reads csv and places into a dictionary
        with open(data, newline = '') as csvfile:
            data_dict = csv.DictReader(csvfile)
            for row in csvfile:
                row['Time_Start'],row['Flight State'],row['exp time'],row['Altitude'], \
                row['Velocity_X'],row['Velocity_Y'],row['Velocity_Z'],row['Attitude_X'],row['Attitude_Y'],row['Attitude_Z'], \
                row['Acceleration_X'],row['Acceleration_Y'],row['Acceleration_Z'],row['Ang_Vel_X'],row['Ang_Vel_Y'],row['Ang_Vel_Z'], \
                row['Liftoff Warning'],row['RCS Warning'],row['Escape Warning'],row['Chute Warning'],row['Landing Warning'],row['Fault Warning'], \
                row['Frequency Measure'],row['Magnetometer'],row['Current'],row['Voltage'],row['Timer'], \
                row['BD_Acceleration_X'],row['BD_Acceleration_Y'],row['BD_Acceleration_Z'], \
                row['BD_Ang_Vel_X'],row['BD_Ang_Vel_Y'],row['BD_Ang_Vel_Z'],row['MOSFET'],row['Time_End']
            #Note: Add Blue Dawn Errors to dictionary if they end up in CSV
            #Last 3 rows report Blue Dawn data. Order may need to be changed depending on final CSV data order.
            #Question: How often is the CSV updated? This model assumes all data at a given time is reported in one row of the CSV 
            limits = []
            for i 
            
