#!/usr/bin/python

""" nff-sample.py
Z Porter
NanoRacks LLC

Version 2.0
Last updated: 2-11-19

Sample python code for NanoLab payload on the NanoRacks Feather Frame. Program opens
up a serial connection and listens to decode any incoming feather frame packets. Default
values and ports are especially for use on a raspberry pi zero through the UART0 interface.
All code is provided as-is by NanoRacks to help customers develop flight code for their 
Feather Frame payloads as quickly and easily as possible.

Note:
  - Use pip to download the pyserial library (pip install pyserial) if it's missing.
  - For pi zero, a line must be added to /etc/rc.local to run the python script on 
  startup. For example: python /home/pi/nff-sample.py &. The ending & runs the program
  in the background.
"""


import time
import serial


MAXBUFFER = 200
NUMDATAFIELDS = 21

# This is specific to the pi zero. Must have serial enabled and console over serial disabled.
PORTNAME = '/dev/ttyAMA0'

BAUDRATE = 115200
TIMEOUT = 0.02

# Dictionary to hold all of the current flight information.
FLIGHT_DATA = {'flight_event': 0, 
                'exptime': 0,
                'altitude': 0,
                'gps_altitude': 0,
                'velocity': [0,0,0],
                'acc_magnitude': 0,
                'acceleration': [0,0,0],
                'attitude': [0,0,0],
                'angular_velocity': [0,0,0],
                'warnings': [0,0,0,0]}


""" parse_serial_packet
Parses the incoming serial packet and updates the flight data

Arguments:
    incoming_data = string of serial data.
Returns:
    true or false depending on successful parsing or not.
"""
def parse_serial_packet(incoming_data):
    # Remove leading or trailing white space and separate the fields.
    incoming_data = incoming_data.strip()
    fields = incoming_data.split(',')

    # Ensure that the appropriate number of data fields are present.
    if len(fields) != NUMDATAFIELDS:
        return False
    else:
        index = 0
        for field in fields:
            if index == 0:
                FLIGHT_DATA['flight_event'] = field
            elif index == 1:
                FLIGHT_DATA['exptime'] = float(field)
            elif index == 2:
                FLIGHT_DATA['altitude'] = float(field)
            elif index == 3:
                FLIGHT_DATA['gps_altitude'] = float(field)
            elif index == 4:
                FLIGHT_DATA['velocity'][0] = float(field)
            elif index == 5:
                FLIGHT_DATA['velocity'][1] = float(field)
            elif index == 6:
                FLIGHT_DATA['velocity'][2] = float(field)
            elif index == 7:
                FLIGHT_DATA['acc_magnitude'] = float(field)
            elif index == 8:
                FLIGHT_DATA['acceleration'][0] = float(field)
            elif index == 9:
                FLIGHT_DATA['acceleration'][1] = float(field)
            elif index == 10:
                FLIGHT_DATA['acceleration'][2] = float(field)
            elif index == 11:
                FLIGHT_DATA['attitude'][0] = float(field)
            elif index == 12:
                FLIGHT_DATA['attitude'][1] = float(field)
            elif index == 13:
                FLIGHT_DATA['attitude'][2] = float(field)
            elif index == 14:
                FLIGHT_DATA['angular_velocity'][0] = float(field)
            elif index == 15:
                FLIGHT_DATA['angular_velocity'][1] = float(field)
            elif index == 16:
                FLIGHT_DATA['angular_velocity'][2] = float(field)
            elif index == 17:
                FLIGHT_DATA['warnings'][0] = int(field)
            elif index == 18:
                FLIGHT_DATA['warnings'][1] = int(field)
            elif index == 19:
                FLIGHT_DATA['warnings'][2] = int(field)
            elif index == 20:
                FLIGHT_DATA['warnings'][3] = int(field)
            index = index + 1
        return True


# Replace this function with proper initialization of experiment.
def init_experiment():
    print("initializing experiment")

# Replace this function with proper experiment starting commands.
def start_experiment():
    print("starting experiment")

# Replace this function with proper experiment stopping commands.
def stop_experiment():
    print("stopping experiment")



""" main

Arguments:
    none
Returns:
    none
"""
def main():
    # Flag to keep track of whether or not experiment has started.
    EXPERIMENT_RUN = False

    # Flag to keep track of whether or not experiment has completed.
    EXPERIMENT_FINISHED = False

    # Wait about 5 seconds before starting (probably unnecessary)
    time.sleep(5)

    # Initialize the experiment.
    init_experiment()

    # Open serial connection. Add more robust error handling to this section if
    # desired.
    ser = serial.Serial(port=PORTNAME, baudrate=BAUDRATE, timeout=TIMEOUT)

    # Main loop to continuously read in incoming data and attempt to parse it.
    while True:
        # Check for any available data in the input serial buffer according to the polling rate.
        while ser.in_waiting == 0:
            time.sleep(0.01)

        # Read in up to the maximum size of data per line.
        data_in = ser.read(MAXBUFFER)

        # Check that some data was received.
        if (len(data_in) == 0):
            continue

        # Check that packet was well formatted.
        if not parse_serial_packet(data_in):
            continue

        # If the experiment hasn't run yet then check against the start conditions
        # to decide if it should be started. Example start condition is altitude >
        # 20000 ft.
        if not EXPERIMENT_RUN:
            if (FLIGHT_DATA['altitude'] > 20000):
                start_experiment()
                EXPERIMENT_RUN = True
        # If the experiment has been run but has not completed yet, then check against
        # the stop condition to decide if it should be finished. Example stop condition
        # is altitude > 50000 ft.
        elif not EXPERIMENT_FINISHED:
            if (FLIGHT_DATA['altitude'] > 50000):
                stop_experiment()
                EXPERIMENT_FINISHED = True


if __name__=="__main__":
    main()
