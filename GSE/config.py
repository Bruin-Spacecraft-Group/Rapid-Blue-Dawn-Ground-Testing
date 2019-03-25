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
#note this list is not used currently
DATA_CSV_MAP = [
    'time_start', 'flight_state', 'exp_time', 'altitude', 'velocity_x', \
    'velocity_y', 'velocity_z', 'attitude_x', 'attitude_y', 'attitude_z', \
    'acceleration_x', 'acceleration_y', 'acceleration_z', 'ang_vel_x', 'ang_vel_y',\
    'ang_vel_z', 'liftoff warning', 'rcs warning', 'escape warning', 'chute warning', \
    'landing warning', 'fault warning', 'frequency measure', 'magnetometer', \
    'current', 'voltage', 'timer', 'sc_acceleration_x', 'sc_acceleration_y', \
    'sc_acceleration_z', 'sc_ang_vel_x', 'sc_ang_vel_y', 'sc_ang_vel_z', 'mosfet', \
    'time_end'
]

#TODO: better limits
#TODO: lower limits? Multiple limit levels?
#map includes names in correct order, paired with upper limit value
PACKETMAP = {
    1:['spacecraft_time',0,1e7],
    2:['sc_acceleration_x',-5, 5], 
    3:['sc_acceleration_y',-5, 5], 
    4:['sc_acceleration_z',-5, 5],
    5:['sc_ang_vel_x',-60, 60], 
    6:['sc_ang_vel_y',-60, 60], 
    7:['sc_ang_vel_z',-60, 60],
    8:['sc_mag_x',-1000,1000],
    9:['sc_mag_y',-1000,1000],
    10:['sc_mag_z',-1000,1000], 
    11:['mosfet_state',0,0.5],  
    12:['flow_rate',0,1000],
    13:['pump_current',250,500],
    14:['pump_voltage',4.9,5.1],
    15:['dt',0,250],
    16:['current',45,800], 
    17:['voltage',4.9,5.1],
    18:['flight_state',-1,100], 
    19:['exp_time',0,1e7], 
    20:['altitude',0,333000], 
    21:['velocity_x',0,3500], 
    22:['velocity_y',0,3500], 
    23:['velocity_z',0,3500], 
    24:['attitude_x',0,1000], 
    25:['attitude_y',0,1000], 
    26:['attitude_z',0,1000], 
    27:['acceleration_x',-5,5], 
    28:['acceleration_y',-5,5],
    29:['acceleration_z',-5,5], 
    30:['ang_vel_x',-60,60], 
    31:['ang_vel_y',-60,60], 
    32:['ang_vel_z',-60,60],
    33:['liftoff_warning',0,0.5], 
    34:['rcs_warning',0,0.5], 
    35:['escape_warning',0,0.5], 
    36:['chute_warning',0,0.5],
    37:['landing_warning',0,0.5], 
    38:['fault_warning',0,0.5]
}