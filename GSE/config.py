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
SERIAL_NFF_SUBSCRIBE = "tcp://localhost:8004"
NFF_PUBLISH = "tcp://*:8004"

#packet information
# #note this list is not used currently
# DATA_CSV_MAP = [
#     'time_start', 'flight_state', 'exp_time', 'altitude', 'velocity_x', \
#     'velocity_y', 'velocity_z', 'attitude_x', 'attitude_y', 'attitude_z', \
#     'acceleration_x', 'acceleration_y', 'acceleration_z', 'ang_vel_x', 'ang_vel_y',\
#     'ang_vel_z', 'liftoff warning', 'rcs warning', 'escape warning', 'chute warning', \
#     'landing warning', 'fault warning', 'frequency measure', 'magnetometer', \
#     'current', 'voltage', 'timer', 'sc_acceleration_x', 'sc_acceleration_y', \
#     'sc_acceleration_z', 'sc_ang_vel_x', 'sc_ang_vel_y', 'sc_ang_vel_z', 'mosfet', \
#     'time_end'
# ]

#map includes names in specific order, paired with lower and upper limit value
UmbilicalMap = {
    'current': [45,800], 
    'voltage': [4.9,5.1],
}

ScMap = {
    'spacecraft_time': [0,1e7],
    'sc_acceleration_x': [-5, 5], 
    'sc_acceleration_y': [-5, 5], 
    'sc_acceleration_z': [-5, 5],
    'sc_ang_vel_x': [-60, 60], 
    'sc_ang_vel_y': [-60, 60], 
    'sc_ang_vel_z': [-60, 60],
    'sc_mag_x': [-1000,1000],
    'sc_mag_y': [-1000,1000],
    'sc_mag_z': [-1000,1000], 
    'mosfet_state': [0,0.5],  
    'flow_rate': [0,1000],
    'pump_current': [250,500],
    'pump_voltage': [4.9,5.1],
    'dt': [0,250],
}

NffMap = {
    'flight_state': [-1,100], 
    'exp_time': [0,1e7], 
    'altitude': [0,333000], 
    'velocity_x': [0,3500], 
    'velocity_y': [0,3500], 
    'velocity_z': [0,3500], 
    'attitude_x': [0,1000], 
    'attitude_y': [0,1000], 
    'attitude_z': [0,1000], 
    'acceleration_x': [-5,5], 
    'acceleration_y': [-5,5],
    'acceleration_z': [-5,5], 
    'ang_vel_x': [-60,60], 
    'ang_vel_y': [-60,60], 
    'ang_vel_z': [-60,60],
    'liftoff_warning': [0,0.5], 
    'rcs_warning': [0,0.5], 
    'escape_warning': [0,0.5], 
    'chute_warning': [0,0.5],
    'landing_warning': [0,0.5], 
    'fault_warning': [0,0.5]
}
