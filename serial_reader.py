import serial
import datetime
#SERIAL_PORT = "COM8"
SERIAL_PORT = input("Serial port of choice: ")

try:
	print("Opening Serial Port...")
	#initiate serial port to read data from
	ser = serial.Serial(
	    port=SERIAL_PORT,
	    baudrate=115200,
	    timeout=3,                         # give up reading after 3 seconds
	    parity=serial.PARITY_ODD,
	    stopbits=serial.STOPBITS_TWO,
	    bytesize=serial.SEVENBITS
	)
	print("connected to port " + SERIAL_PORT)
except:
	print("<== Error connecting to " + SERIAL_PORT + " ==>")
	exit()

##create plain text file to save raw data as backup for database
date = str(datetime.datetime.now())
FILENAME = 'Raw_Data/' + date
FILENAME = FILENAME.replace(':', '_')
txtfile = open(FILENAME, "w")
txtfile.write('Blue Dawn Freq library test starting at ' + date)


print("running")
while ser.isOpen():
	try:
		#get data
		#print('reading...')
		dataString = str(ser.readline())
		print(dataString)
	except:
		print("could not read")
		continue

	try:
		print('Writing to textfile')
		txtfile.write(dataString)
		txtfile.flush()
	except:
		pass
