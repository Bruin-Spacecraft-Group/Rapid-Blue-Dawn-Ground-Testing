# nff-sim.py
# Z Porter
# NanoRacks LLC
# 5-15-17
#
# - Requires nff-packets.txt to be in the same directory
# - Consult the ReadMe.md for further use instructions
#
# Simulates the feather frame data interface to the NanoLabs by connecting to multiple serial devices
# provided by the user and then sending the serial packets contained in the nff-packets.txt file
# at a rate of approximately 10Hz.
####################################################################################################


import time, datetime
import serial
import os
# import msvcrt # Not on windows
import getch

import curses
from curses import panel


PROGRESS_BAR_LENGTH = 80
PACKET_INTERVAL = 0.1
MAXBUFFER = 200
TIMEOUT = 0.02
BAUDRATE=115200
NUMDATAFIELDS = 21

# Used for parsing input from user
import KBhitParser


def printPacket(in_packet, out_packet):

    # Split line input from the arduino
    # Print all of the flight information in an easy to read format
    counter = 1
    for field in in_packet.split(',') :
      if (counter == 1) :
        if (field == '@') :
          print('Flight state: none reached')
        elif (field == 'A') :
          print('Flight state: liftoff')
        elif (field == 'B') :
          print('Flight state: meco')
        elif (field == 'C') :
          print('Flight state: separation')
        elif (field == 'D') :
          print('Flight state: coast_start')
        elif (field == 'E') :
          print('Flight state: apogee')
        elif (field == 'F') :
          print('Flight state: coast_end')
        elif (field == 'G') :
          print('Flight state: under_chutes')
        elif (field == 'H') :
          print('Flight state: landing')
        elif (field == 'I') :
          print('Flight state: safing')
        elif (field == 'J') :
          print('Flight state: finished')
        else :
          print('Flight state: unknown')
      elif (counter == 2) :
        print ('Experiment time: ' + field + ' sec')
      elif (counter == 3) :
        print ('Altitude: ' + field + ' ft')
      elif (counter == 4):
        print ('Velocity:')
        print ('   x-axis: ' + field + ' ft/sec')
      elif (counter == 5):
        print ('   y-axis: ' + field + ' ft/sec')
      elif (counter == 6):
        print ('   z-axis: ' + field + ' ft/sec')
      elif (counter == 7):
        print ('Acceleration:')
        print ('   magnitude: ' + field + ' ft/sec^2')
      elif (counter == 8):
        print ('   not-used: ' + field)
      elif (counter == 9):
        print ('   not-used: ' + field)
      elif (counter == 10):
        print ('Attitude:')
        print ('   x-axis: ' + field + ' radians')
      elif (counter == 11):
        print ('   y-axis: ' + field + ' radians')
      elif (counter == 12):
        print ('   z-axis: ' + field + ' radians')
      elif (counter == 13):
        print ('Angular velocity:')
        print ('   x-axis: ' + field + ' radians/sec')
      elif (counter == 14):
        print ('   y-axis: ' + field + ' radians/sec')
      elif (counter == 15):
        print ('   z-axis: ' + field + ' radians/sec')
      elif (counter == 16):
        if (field == '1') :
          print ('Liftoff warning: true')
        else :
          print ('Liftoff warning: false')
      elif (counter == 17):
        if (field == '1') :
          print ('RCS warning:     true')
        else :
          print ('RCS warning:     false')
      elif (counter == 18):
        if (field == '1') :
          print ('Escape warning:  true')
        else :
          print ('Escape warning:  false')
      elif (counter == 19):
        if (field == '1') :
          print ('Chute warning:   true')
        else :
          print ('Chute warning:   false')
      elif (counter == 20):
        if (field == '1') :
          print ('Landing warning: true')
        else :
          print ('Landing warning: false')
      elif (counter == 21):
        if (field == '1') :
          print ('Fault warning:   true')
        else :
          print ('Fault warning:   false')

      counter += 1

    print('')



def main():

  # Array for holding serial connections.
  ser = []



  # Display welcome message.
  print('****************************************')
  print('**    Welcome to the NFF simulator    **')
  print('**            NanoRacks LLC           **')
  print('**     Consult the ReadMe.md for      **')
  print('**           use instructions         **')
  print('****************************************')
  print('')

  # Prompt user for the com ports to connect to.
  myinput = input('Enter the ports to connect to: ')
  print('')

  # Try to connect to each of the com ports provided by the user. If the
  # connection was successful then add it to the array of serial connections.
  for port in myinput.split() :
    try :
      temp = serial.Serial(port=port, baudrate=BAUDRATE, timeout=TIMEOUT)
      ser.append(temp)
      print('Successfully connected to: ' + port)
    
    except :
      print('Failed to connect to: ' + port)
  print('')

  # If no connections are made then tell the user and exit the program.
  if len(ser) == 0 :
    print('Error: no connections established')
    print('Check the com port and ensure no other programs are connected to it')
    print('')
    discard = input('Press <enter> to exit')
    return

  # Try to open the text file with all of the packets to send and exit
  # if it fails to open.
  try:
    infile = open('nff-packets.txt', 'r')

  except:
    print('Error: couldn\'t open nff-packets.txt')
    print('Make sure the file is in the same directory as the .exe')
    print('')
    discard = input('Press <enter> to exit')
    return


  # Try and open output file
  try:
    timestr = time.strftime("%d-%b-%Y_%H:%M:%S", time.localtime())
    outfile = open("log/" + timestr + "_log.txt",  "w+")

  except:
    print('Error: couldn\'t open logfile')
    print('')
    discard = input('Press <enter> to exit')
    return

  # Parser for compatibility with non-windows machines
  kb = KBhitParser.KBHit()

  # Make sure files are open
  time.sleep(0.1)

  # Wait until user is ready to start the simulation.
  input('Press <enter> to start the simulation!')

  

  # Current speed of the simulation, 1 is normal, 2 is twice as fast, etc.
  speed = 1


  '''
  Main program loop
  
  Loops through every line in packets

  Send line only when time since last packet exceed interval

  Check for response from Arduino (Data received)

  '''

  # Counter variable for number of packets sent.
  packet_counter = 0

  # Read all of the packets and store the total number to keep track of progress.
  all_lines = infile.readlines()
  num_lines = len(all_lines)

  prev_time = datetime.datetime.utcnow().timestamp()
  out_packet = all_lines[0]
  in_packet = ""
  packets_received = 0

  # Main Loop

  while packet_counter < num_lines:

    # Send packet if time interval is met
    curr_time = datetime.datetime.utcnow().timestamp()
    if curr_time - prev_time > PACKET_INTERVAL:

      line = all_lines[packet_counter]
      packet = line.rstrip()

      # Send the packet to each connected device.
      for devs in ser :
        devs.write(packet.encode())

      out_packet = line
      prev_time = curr_time
      packet_counter += speed


    # Check for keystroke input from user
    if kb.kbhit() :
      # Retrieve the key pressed
      key = ord(kb.getch())
      
      # Check if 'q' was pressed
      if key == 113 :
        break
      # Check if 'p' was pressed
      elif key == 112 :
        print('')
        input("Simulation paused, press <enter> to unpause.")
      # Check if a or d was entered, for fast forwarding or slowing it down
      elif (key == 97) and (speed != 1):
        # 'a' slows down (min is x1).
        speed = speed / 2
      elif (key == 100) and (speed != 16):
        # 'd' speeds up (max is x16).
        speed = speed * 2

    # Listen for response from Arduino

    # Read in up to the maximum size of data per line.
    # 0 is used because we only have 1 arduinp
    data_in = ser[0].read(MAXBUFFER).decode('ascii')
    ser[0].reset_input_buffer()

    # Strip newline characters
    data_in = data_in.rstrip('\n')
    data_in = data_in.rstrip('\r')
    data_in = data_in.rstrip('\n')

    # Check that some data was received.
    if (len(data_in) != 0):
      in_packet = data_in

    if(len(data_in.split(",")) == NUMDATAFIELDS):
      packets_received += 1


    # Output contents to logfile
    outfile.write(in_packet + "\n")

    # Clear the terminal so output is printed in the same position each iteration
    os.system('clear')

    # Cool running effect with the dots.
    print('NFF simulation running' + ('.' * (int)((packet_counter % 12) / 3)))
    print('')

    # Display all of the connected ports.
    for devs in ser:
      print ('Connected to: ' + devs.port)
    print('')

    # Display the current packet being sent.
    print('Sending packet: ' + out_packet)
    print('')

    # Print packet received from arduino
    print("Length: %d" % (len(in_packet.split(","))))
    print("Packet received: " + in_packet)

    # Companre number of packets received to packets sent
    print("Packets sent: %d" % (packet_counter))
    print("Packets received: %d" % (packets_received))
    print('')

    # Print contents of packet to console
    printPacket(in_packet, out_packet)

    

    # Display how far along the simulation is with a neat loading bar (the magic 20 number is to
    # prevent the simulation from obnoxiously ending while displaying 99%, I'm a little OCD).
    print('Simulation progress: [' + '#' * (int)(packet_counter / (num_lines / PROGRESS_BAR_LENGTH)) 
          + ' ' * (int)(PROGRESS_BAR_LENGTH - (packet_counter / (num_lines / PROGRESS_BAR_LENGTH))) + '] ' 
          + str(((100 * (int)(packet_counter + 20)) / num_lines)) + '%')
    print('')

    # Display the current speed the simulation is running at.
    print('Current speed: x' + str(speed))
    print('Press a to slow down sim or d to speed up sim')
    print('')

    # Inform user about option to quit
    print('Press <q> at any time to quit or <p> to pause')

    time.sleep(0.01)


  # Close all device connections after simulation has finished.
  for devs in ser :
    devs.close()

  # Close files
  infile.close()
  outfile.close()

  # Inform the user that the simulation has finished and wait for them to press enter and exit.
  print('')
  print('NFF simulation completed!')
  discard = input('Press <enter> to exit')
  print('\n')

main()