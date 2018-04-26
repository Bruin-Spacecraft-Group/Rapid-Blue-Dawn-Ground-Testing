import serial, os
from time import sleep

# CONSTANTS
TIMEOUT = 0.02
BAUDRATE = 115200
BUFSIZE = 200
TEST_STRING = 'The quick brown fox jumps over the lazy dog 1234567890.,'

def print_welcome_msg():
	print('****************************************')
	print('**     Project Rapid Ground Testing   **')
	print('**               FC ISTM              **')
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
		print('Sending Test String: ' + TEST_STRING)
		ard_serial.write(TEST_STRING.encode())

		sleep(0.5)

		try: 
			data_in = ard_serial.readline(BUFSIZE).decode()

			# Strip newline characters
			data_in = data_in.rstrip('\n')
			data_in = data_in.rstrip('\r')
			data_in = data_in.rstrip('\n')

			if(data_in == TEST_STRING):
				done = True

			print('Received: ' + data_in)
		except:
			pass

		sleep(0.5)

	print('Test successful!')
	ard_serial.close()
	discard = input('Press <enter> to exit...')

if __name__ == '__main__':
	main()