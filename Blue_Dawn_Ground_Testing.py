import serial
import sys
import time
import os

MAXBUFFER = 200
NUMDATAFIELDS = 21

# Dictionary to hold all of the current flight information.
FLIGHT_DATA = {'flight_state': 0, 
				'exptime': 0,
				'altitude': 0,
				'velocity': [0,0,0],
				'acceleration': [0,0,0],
				'attitude': [0,0,0],
				'angular_velocity': [0,0,0],
				'warnings': [0,0,0,0,0,0]}

BAUDRATE = 115200
TIMEOUT = 0.02

errorlog = None

""" parse_serial_packet
Parses the incoming serial packet and updates the flight data

Arguments:
	incoming_data = string of serial data.
Returns:
	true or false depending on successful parsing or not.
"""
def parse_serial_packet(incoming_data, packet_no):
	# Remove leading or trailing white space and separate the fields.
	incoming_data = incoming_data.strip()
	fields = incoming_data.decode('ascii').split(',')

	# Ensure that the appropriate number of data fields are present.
	if len(fields) != NUMDATAFIELDS:
		return False
	else:
		index = 0

		for field in fields:

			if field == "":
				field = "0"

			if index == 0:
				FLIGHT_DATA['flight_state'] = field
			elif index == 1:
				FLIGHT_DATA['exptime'] = float(field)
			elif index == 2:
				FLIGHT_DATA['altitude'] = float(field)
			elif index == 3:
				FLIGHT_DATA['velocity'][0] = float(field)
			elif index == 4:
				FLIGHT_DATA['velocity'][1] = float(field)
			elif index == 5:
				FLIGHT_DATA['velocity'][2] = float(field)
			elif index == 6:
				FLIGHT_DATA['acceleration'][0] = float(field)
			elif index == 7:
				FLIGHT_DATA['acceleration'][1] = float(field)
			elif index == 8:
				FLIGHT_DATA['acceleration'][2] = float(field)
			elif index == 9:
				FLIGHT_DATA['attitude'][0] = float(field)
			elif index == 10:
				FLIGHT_DATA['attitude'][1] = float(field)
			elif index == 11:
				FLIGHT_DATA['attitude'][2] = float(field)
			elif index == 12:
				FLIGHT_DATA['angular_velocity'][0] = float(field)
			elif index == 13:
				FLIGHT_DATA['angular_velocity'][1] = float(field)
			elif index == 14:
				FLIGHT_DATA['angular_velocity'][2] = float(field)
			elif index == 15:
				FLIGHT_DATA['warnings'][0] = int(field)
			elif index == 16:
				FLIGHT_DATA['warnings'][1] = int(field)
			elif index == 17:
				FLIGHT_DATA['warnings'][2] = int(field)
			elif index == 18:
				FLIGHT_DATA['warnings'][3] = int(field)
			elif index == 19:
				FLIGHT_DATA['warnings'][4] = int(field)
			elif index == 20:
				FLIGHT_DATA['warnings'][5] = int(field)
			index = index + 1

		return True


def cleanUp():
	print("Experiment finished. Goodbye!")
	sys.exit(0)


def main():

	serialPort = input("Please input Arduino serial port: ")

	read_buf = ""

	ard = serial.Serial(port=serialPort, baudrate=BAUDRATE, timeout=TIMEOUT)

	if not ard.is_open:
		print("Unable to connect to serial port. Exiting.")
		sys.exit(1)

	EXIT_CONDITION_MET = False

	packet_no = 1

	# Program Loop
	while not EXIT_CONDITION_MET:

		try: 
			# Run the loop at roughly 100Hz.
			time.sleep(0.01)

			# Read in up to the maximum size of data per line.
			data_in = ard.read(MAXBUFFER)

			# Check that some data was received.
			if (len(data_in) == 0):
				# print("Waiting for data...")
				continue

			parse_serial_packet(data_in, packet_no)

			# Print data received
			os.system('clear')
			print(FLIGHT_DATA)

			packet_no += 1

			# Check if exit condition is met
			if(FLIGHT_DATA['flight_state'] == "J" ):
				ard.close()
				EXIT_CONDITION_MET = True

		except KeyboardInterrupt:
			ard.close()
			print("Keyboard interrupt")
			sys.exit(1)

		except:
			print("Error handling data")
			print(data_in)
			# ard.close()
			# sys.exit(1)


	cleanUp()


if __name__ == '__main__':
	main()


