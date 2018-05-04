import serial, os
from time import sleep

# CONSTANTS
TIMEOUT = 0.02
BAUDRATE = 115200
BUFSIZE = 200

def print_welcome_msg():
	print('****************************************')
	print('**     Project Rapid Ground Testing   **')
	print('**            FC_Functional           **')
	print('**               v0.1.0               **')
	print('****************************************')

def main():

	print_welcome_msg()
	
	ard_port = input('Enter the Arduino serial port: ')
	ard_port = ard_port.strip()

	try:
		ard_serial = serial.Serial(port=ard_port, baudrate=BAUDRATE, timeout=TIMEOUT)
		print('Successfully connected to ' + ard_port + '!')
	except:
		print('Unable to connect to serial port. Check Arduino serial port connection. ')
		return

	discard = input('Press <enter> to begin the test!')

	done = False
	
	while not done:

		try: 
			data_in = ard_serial.readline(BUFSIZE).decode()

			# Strip newline characters
			data_in = data_in.rstrip('\n')
			data_in = data_in.rstrip('\r')
			data_in = data_in.rstrip('\n')

			print('Arduino Time: ' + data_in)

		except:
			pass

		sleep(0.5)

	print('Test successful!')
	ard_serial.close()
	discard = input('Press <enter> to exit...')

if __name__ == '__main__':
	main()