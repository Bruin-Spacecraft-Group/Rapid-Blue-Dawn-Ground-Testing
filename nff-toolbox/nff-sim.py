# nff-sim.py
# Z Porter
# NanoRacks LLC
#
# Version 2.0
# Last Updated: 2-11-19
#
# - Requires nff-packets.txt to be in the same directory
# - Consult the ReadMe.md for further use instructions
#
# Simulates the feather frame data interface to the NanoLabs by connecting to multiple serial devices
# provided by the user and then sending the serial packets contained in the nff-packets.txt file
# at a rate of approximately 10Hz.
####################################################################################################


import time
import serial
import os
import msvcrt


PROGRESS_BAR_LENGTH = 80


def main():
  # Array for holding serial connections.
  ser = []

  # Display welcome message.
  print('****************************************')
  print('**    Welcome to the NFF simulator    **')
  print('**            NanoRacks LLC           **')
  print('**     Consult the README.md for      **')
  print('**           use instructions         **')
  print('****************************************')
  print('')

  # Prompt user for the com ports to connect to.
  input = raw_input('Enter the ports to connect to: ')
  print('')

  # Try to connect to each of the com ports provided by the user. If the
  # connection was successful then add it to the array of serial connections.
  for port in input.split() :
    try :
      temp = serial.Serial(port, 115200)
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
    discard = raw_input('Press <enter> to exit')
    return

  # Try to open the text file with all of the packets to send and exit
  # if it fails to open.
  try:
    infile = open('nff-packets.txt', 'r')

  except:
    print('Error: couldn\'t open nff-packets.txt')
    print('Make sure the file is in the same directory as the .exe')
    print('')
    discard = raw_input('Press <enter> to exit')
    return

  # Counter variable for number of packets sent.
  packet_counter = 0

  # Read all of the packets and store the total number to keep track of progress.
  all_lines = infile.readlines()
  num_lines = len(all_lines)

  # Wait until user is ready to start the simulation.
  raw_input('Press <enter> to start the simulation!')

  # Current speed of the simulation, 1 is normal, 2 is twice as fast, etc.
  speed = 1

  # Iterate through all of the packets (Main simulation loop).
  for lines in all_lines :
    # The higher the speed, the more packets are skipped over.
    if not ((packet_counter % speed) == 0):
      packet_counter += 1
      continue

    # Strip any new line or white space off the end of the line.
    packet = lines.rstrip()

    # Check for keystrokes and if 'q' is entered then exit the loop.
    if msvcrt.kbhit() :
      # Retrieve the key pressed
      key = ord(msvcrt.getch())
      
      # Check if 'q' was pressed
      if key == 113 :
        break
      # Check if 'p' was pressed
      elif key == 112 :
        print('')
        raw_input("Simulation paused, press <enter> to unpause.")
      # Check if <- or -> was entered, both arrows have two codes that must be
      # retrieved and both begin with 0 or 224.
      elif (key == 0) or (key == 224):
        # Retrieve the second key code for special keys.
        key = ord(msvcrt.getch())

        # Left arrow code slows down (min is x1).
        if (key == 75) and (speed != 1) :
          speed = speed / 2
        # Right arrow code speeds up (max is x16).
        elif (key == 77) and (speed != 16) :
          speed = speed * 2

    # Clear the terminal so output is printed in the same position each iteration
    os.system('cls')

    # Cool running effect with the dots.
    print('NFF simulation running' + '.' * ((packet_counter % 12) / 3))
    print('')

    # Display all of the connected ports.
    for devs in ser:
      print ('Connected to: ' + devs.port)
    print('')

    # Display the current packet being sent.
    print('Sending packet: ' + packet)
    print('')

    # Print all of the flight information in an easy to read format
    counter = 1
    for field in lines.split(',') :
      if (counter == 1) :
        if (field == '@') :
          print('Flight event: none reached')
        elif (field == 'A') :
          print('Flight event: escape enabled')
        elif (field == 'B') :
          print('Flight event: escape commanded')
        elif (field == 'C') :
          print('Flight event: liftoff')
        elif (field == 'D') :
          print('Flight event: meco')
        elif (field == 'E') :
          print('Flight event: separation')
        elif (field == 'F') :
          print('Flight event: coast start')
        elif (field == 'G') :
          print('Flight event: apogee')
        elif (field == 'H') :
          print('Flight event: coast end')
        elif (field == 'I') :
          print('Flight event: drogue chutes')
        elif (field == 'J') :
          print('Flight event: main chutes')
        elif (field == 'K') :
          print('Flight event: touchdown')
        elif (field == 'L') :
          print('Flight event: safing')
        elif (field == 'M') :
          print('Flight event: mission end')
        else :
          print('Flight event: unknown')
      elif (counter == 2) :
        print ('Experiment time: ' + field + ' sec')
      elif (counter == 3) :
        print ('Altitude: ' + field + ' ft')
      elif (counter == 4):
        print ('GPS altitude: ' + field + ' ft')
      elif (counter == 5):
        print ('Velocity:')
        print ('   Up: ' + field + ' ft/sec')
      elif (counter == 6):
        print ('   East: ' + field + ' ft/sec')
      elif (counter == 7):
        print ('   North: ' + field + ' ft/sec')
      elif (counter == 8):
        print ('Acceleration:')
        print ('   magnitude: ' + field + ' ft/sec^2')
      elif (counter == 9):
        print ('   x-axis: ' + field + ' ft/sec^2')
      elif (counter == 10):
        print ('   y-axis: ' + field + ' ft/sec^2')
      elif (counter == 11):
        print ('   z-axis: ' + field + ' ft/sec^2')
      elif (counter == 12):
        print ('Attitude:')
        print ('   phi: ' + field + ' radians')
      elif (counter == 13):
        print ('   theta: ' + field + ' radians')
      elif (counter == 14):
        print ('   psi: ' + field + ' radians')
      elif (counter == 15):
        print ('Angular velocity:')
        print ('   x-axis: ' + field + ' radians/sec')
      elif (counter == 16):
        print ('   y-axis: ' + field + ' radians/sec')
      elif (counter == 17):
        print ('   z-axis: ' + field + ' radians/sec')
      elif (counter == 18):
        if (field == '1') :
          print ('Liftoff Imminent warning:       true')
        else :
          print ('Liftoff Imminent warning:       false')
      elif (counter == 19):
        if (field == '1') :
          print ('Drogue Chute Imminent warning:  true')
        else :
          print ('Drogue Chute Imminent warning:  false')
      elif (counter == 20):
        if (field == '1') :
          print ('Landing Imminent warning:       true')
        else :
          print ('Landing Imminent warning:       false')
      elif (counter == 21):
        if (field == '1') :
          print ('Chute Fault warning:            true')
        else :
          print ('Chute Fault warning:            false')

      counter += 1

    print('')

    # Display how far along the simulation is with a neat loading bar (the magic 20 number is to
    # prevent the simulation from obnoxiously ending while displaying 99%, I'm a little OCD).
    print('Simulation progress: [' + '#' * (packet_counter / (num_lines / PROGRESS_BAR_LENGTH)) 
          + ' ' * (PROGRESS_BAR_LENGTH - (packet_counter / (num_lines / PROGRESS_BAR_LENGTH))) + '] ' 
          + str(((100 * (packet_counter + 20)) / num_lines)) + '%')
    print('')

    # Display the current speed the simulation is running at.
    print('Current speed: x' + str(speed))
    print('Press <- to slow down sim or -> to speed up sim')
    print('')

    # Inform user about option to quit
    print('Press <q> at any time to quit or <p> to pause')
    
    # Send the packet to each connected device.
    for devs in ser :
      devs.write(packet)

    # Increment the packet counter.
    packet_counter += 1

    # Delay is chosen to result in a send rate of roughly 10Hz, call isn't very precise at ms level.
    time.sleep(0.07)

  # Close all device connections after simulation has finished.
  for devs in ser :
    devs.close()

  # Inform the user that the simulation has finished and wait for them to press enter and exit.
  print('')
  print('NFF simulation completed!')
  discard = raw_input('Press <enter> to exit')

main()