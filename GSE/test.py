import zmq
import config
import time
from random import Random

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind(config.SERIAL_PUBLISH)

x = 0

while True:
    print("sending..")
    if x < 10:
        x += 1
    else:
        x = 0
    val1 = x
    val2 = 0.5*x
    val3 = x*x
    val4 = 2*x

    socket.send_string("{},{},{},{},0,0,{},2,3,4,5,6,{},8,9,1,1,2,3,4,5,6,7,{},4,3,2,1, {},2,{},7,6,5,4,{},1,{},0".format(val1, val2, val3, val4, val2, val3, val4, val1, val4, val3, val2))
    time.sleep(1)