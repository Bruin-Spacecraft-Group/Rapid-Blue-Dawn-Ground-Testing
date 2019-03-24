#serial configs
TIMEOUT = 0.02
BAUDRATE = 115200

#ports
SERIAL_SUBSCRIBE = "tcp://localhost:8000"
SERIAL_PUBLISH = "tcp://*:8001"
SERVER_SUBSCRIBE = "tcp://localhost:8001"
SERVER_PUBLISH = "tcp://*:8002"
GUI_SUBSCRIBE = "tcp://localhost:8002"
GUI_PUBLISH = "tcp://*:8003"
COMMANDER_SUBSCRIBE = "tcp://localhost:8002"
COMMANDER_PUBLISH = "tcp://*:8000"

#packet information
#note this list is not used currently
DATA_CSV_MAP = [
    'time_start', 'flight_state', 'exp_time', 'altitude', 'velocity_x', \
    'velocity_y', 'velocity_z', 'attitude_x', 'attitude_y', 'attitude_z', \
    'acceleration_x', 'acceleration_y', 'acceleration_z', 'ang_vel_x', 'ang_vel_y',\
    'ang_vel_z', 'liftoff warning', 'rcs warning', 'escape warning', 'chute warning', \
    'landing warning', 'fault warning', 'frequency measure', 'magnetometer', \
    'current', 'voltage', 'timer', 'bd_acceleration_x', 'bd_acceleration_y', \
    'bd_acceleration_z', 'bd_ang_vel_x', 'bd_ang_vel_y', 'bd_ang_vel_z', 'mosfet', \
    'time_end'
]

#TODO: better limits
#TODO: lower limits? Multiple limit levels?
#map includes names in correct order, paired with upper limit value
PACKETMAP = {
    'spacecraft_time':1e7,
    'bd_acceleration_x':5, 
    'bd_acceleration_y':5, 
    'bd_acceleration_z':5,
    'bd_ang_vel_x':1000, 
    'bd_ang_vel_y':1000, 
    'bd_ang_vel_z':1000,
    'bd_mag_x':1000,
    'bd_mag_y':1000,
    'bd_mag_z':1000, 
    'mosfet_state':1,  
    'flow_rate':1000,
    'timer':1e7,
    'dt':1e7,
    'voltage':10000,
    'current':10000, 
    'flight_state':-1, 
    'exp_time':1e7, 
    'altitude':333000, 
    'velocity_x':3500, 
    'velocity_y':3500, 
    'velocity_z':3500, 
    'attitude_x':1000, 
    'attitude_y':1000, 
    'attitude_z':1000, 
    'acceleration_x':5, 
    'acceleration_y':5,
    'acceleration_z':5, 
    'ang_vel_x':1000, 
    'ang_vel_y':1000, 
    'ang_vel_z':1000,
    'liftoff_warning':1, 
    'rcs_warning':1, 
    'escape_warning':1, 
    'chute_warning':1,
    'landing_warning':1, 
    'fault_warning':1
}

packetMap = ["spacecraft_time", "flow_rate", "mosfet_state", "timer", "current", "voltage"]
