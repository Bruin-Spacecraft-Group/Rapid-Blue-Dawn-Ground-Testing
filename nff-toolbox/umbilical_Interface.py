import serial

def initUmbilical():
	myPort = 'COM7'
	try:
		print("Opening Serial Port...")
		#initiate serial port to read data from
		umbilicalSer = serial.Serial(
		    port=myPort,
		    baudrate=9600,
		    timeout=5, #give up reading after 5 seconds
		    parity=serial.PARITY_ODD,
		    stopbits=serial.STOPBITS_TWO,
		    bytesize=serial.SEVENBITS
		)
		print("connected to port " + myPort)
		return umbilicalSer
	except:
		print("<== Error connecting to " + myPort + " ==>")
		exit()


def readUmbilicalData(umbilicalSer):
	umbilicalData = []
	spot = 0
	while umbilicalSer.isOpen():
		dataString = ''
		try:
			#get data
			dataString = str(umbilicalSer.readline())
			#print(dataString)
		except:
			print("could not read")
			continue
			
		try:
			#cut off extra characters
			#first two characters are b'
			#last 5, are \r\n'
			dataString = dataString[2:len(dataString)-5]
			data = dataString.split(":")
			print(data)
			if data[0] == 'Bus Voltage':
				spot = 0
			elif data[0] == 'Shunt Voltage':
				spot = 1
			elif data[0] == 'Load Voltage':
				spot = 2
			elif data[0] == 'Current':
				spot = 3
			elif data[0] == 'Power':
				spot = 4
			else:
				continue

			umbilicalData[spot] = [data[0], data[1]]

			if spot == 4:
				spot = 0
				return umbilicalData
			else:
				spot += 1
				continue
		except:
			print('error handling data')

ser = initUmbilical()
while True:
	myData = readUmbilicalData(ser)
	#print(myData)
	pass