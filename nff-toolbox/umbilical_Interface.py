import serial

def initUmbilical():
	myPort = 'COM7'
	try:
		print("Opening Serial Port...")
		#initiate serial port to read data from
		umbilicalSer = serial.Serial(
		    port=myPort,
		    baudrate=115200,
		    timeout=5, #give up reading after 5 seconds
		    parity=serial.PARITY_ODD,
		    stopbits=serial.STOPBITS_TWO,
		    bytesize=serial.SEVENBITS
		)
		print("connected to port " + myPort)
		return umbilicalSer
	except:
		print("<== Error connecting to umbilical at " + myPort + " ==>")
		exit()


def readUmbilicalData(umbilicalSer):
	umbilicalData = {'Bus Voltage': 0,'Shunt Voltage': 0, 'Load Voltage': 0, 'Current': 0, 'Power': 0}
	n = 0

	while umbilicalSer.isOpen():
		dataString = ''
		try:
			#get data
			dataString = umbilicalSer.readline().decode('utf-8')
			#print(dataString)
		except:
			print("could not read umbilical data")
			continue
			
		try:
			#cut off extra characters leftover from arduino serial
			#first two characters are b'
			#last 5, are \r\n'
			#dataString = dataString[2:len(dataString)-5]
			data = dataString.split(":")
			
			if data[0] == 'Bus Voltage':
				umbilicalData['Bus Voltage'] = removeExtraSpaces(data[1])
			elif data[0] == 'Shunt Voltage':
				umbilicalData['Shunt Voltage'] = removeExtraSpaces(data[1])
			elif data[0] == 'Load Voltage':
				umbilicalData['Load Voltage'] = removeExtraSpaces(data[1])
			elif data[0] == 'Current':
				umbilicalData['Current'] = removeExtraSpaces(data[1])
			elif data[0] == 'Power':
				umbilicalData['Power'] = removeExtraSpaces(data[1])
			else:
				continue

			if n == 4:
				return umbilicalData
			else:
				n += 1
				continue
		except:
			print('error handling data')
			return {}

def removeExtraSpaces(str):
	for i in str:
		if i == ' ':
			str = str[1:]
		else:
			return str