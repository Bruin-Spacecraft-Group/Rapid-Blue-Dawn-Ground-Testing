import serial

from sys import argv

# Prints usage for program
def printUsage():
	print('Usage: python3 Blue_Dawn_Ground_Testing.py -i <arduino_serial_port>')

# Function for getting arguments
def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def main():
	myargs = getopts(argv)

	if '-i' in myargs:
		print(myargs['-i'])
	else:
		printUsage()
		return

	read_buf = ""

	er = serial.Serial('COM3', 38400, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

if __name__ == '__main__':
	main()


