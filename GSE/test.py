import zmq
import config
import time
from random import Random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(config.SERIAL_PUBLISH)
#socket.bind('tcp://*:5555')

x = 0

while True:
    print("sending..")
    if x < 10:
        x += 1
    else:
        x = 0
    val1 = x
    val2 = 0.5*x
    val3 = Random(x)
    val4 = "my val is {}".format(x)

    socket.send_string("{},{},{},{},test,test".format(val1, val2, val3, val4))
    time.sleep(1)