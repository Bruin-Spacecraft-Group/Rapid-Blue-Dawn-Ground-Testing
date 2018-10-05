import serial.tools.list_ports as list_serial_ports
import subprocess
import sys
import time
import atexit

def launchGUI():
    ## launch on different thread, return a Popen object to close later, pip output to stdout
    return(subprocess.Popen([sys.executable, 'gui.py'], stdout=subprocess.PIPE))

def launchServer():
    ## launch on different thread, return a Popen object to close later, pip output to stdout
    return(subprocess.Popen([sys.executable, 'server.py'], stdout=subprocess.PIPE))

def launchSerialManager():
    print('List of Serial Devices Found:')
    for x in list_serial_ports.comports():
        ## serial.tools.list_ports returns serialPort objects
        ## take the names of each first one
        print(x[0])
    print()
    bd = input('Blue Dawn Serial: ')
    um = input('Umbilical Serial: ')

    ## launch on different thread, return Popen object to close later, pipe output to stdout
    return(subprocess.Popen([sys.executable, 'serial_manager.py', bd, um], stdout=subprocess.PIPE))

def exit(ts):
    for t in ts:
        t.terminate()

if __name__ == '__main__':
    threads = [launchGUI(), launchServer(), launchSerialManager()]
    ## register exit to run before quit on threads
    atexit.register(exit, threads)
    while(True):
        time.sleep(5)
