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
import sys
import zmq
from zmq import ZMQError
from PyQt5.Qt import QThread, QListWidgetItem

PROGRESS_BAR_LENGTH = 80

class NFFSim(QThread):
  def __init__(self, parent_ui, nff_publish):
    QThread.__init__(self)
    self.ui = parent_ui

    try:
      context = zmq.Context()
      self.publish_socket = context.socket(zmq.PUB)
      self.publish_socket.bind(nff_publish)
    except:
      print("ERROR: Cannot connect to sockets!")
      sys.exit()
  
    # Try to open the text file with all of the packets to send and exit
    # if it fails to open.
    try:
      infile = open('nff-packets.txt', 'r')

    except:
      print('Error: couldn\'t open nff-packets.txt')
      return

    # Read all of the packets and store the total number to keep track of progress.
    self.all_lines = infile.readlines()
    self.num_lines = len(self.all_lines)

    # init UI
    self.ui.nff_sim_progress_bar.setValue(0)
    self.console = self.ui.nff_console

  def run(self):
    self.Active = True
    self.paused = False
    # Counter variable for number of packets sent.
    self.packet_counter = 0

    while self.packet_counter <= self.num_lines:
      if not self.paused:
        # Current speed of the simulation, 1 is normal, 2 is twice as fast, etc.
        self.speed = self.ui.sim_speed.value()
        # The higher the speed, the more packets are skipped over.
        if not ((self.packet_counter % self.speed) == 0):
          self.packet_counter += 1
          continue
        self.advanceSim(self.all_lines[self.packet_counter])
        self.packet_counter += 1
        #self.console.scrollToBottom()
      else:
        time.sleep(0.25)
    # Inform the user that the simulation has finished and wait for them to press enter and exit.
    self.console.addItem(QListWidgetItem(''))
    self.console.addItem(QListWidgetItem('NFF simulation completed!'))


  def pause(self):
    if self.paused:
      self.paused = False
      self.console.addItem(QListWidgetItem("resume sim"))
    else:
      self.paused = True
      self.console.addItem(QListWidgetItem("pause sim"))
    

  def advanceSim(self, line):
    # Strip any new line or white space off the end of the line.
    packet = line.rstrip()
    if (self.packet_counter % 10 == 0):
      #print(packet)
      self.console.addItem(QListWidgetItem(packet))


    # # Print all of the flight information in an easy to read format
    # counter = 1
    # for field in lines.split(',') :
    #   if (counter == 1) :
    #     if (field == '@') :
    #       print('Flight event: none reached')
    #     elif (field == 'A') :
    #       print('Flight event: escape enabled')
    #     elif (field == 'B') :
    #       print('Flight event: escape commanded')
    #     elif (field == 'C') :
    #       print('Flight event: liftoff')
    #     elif (field == 'D') :
    #       print('Flight event: meco')
    #     elif (field == 'E') :
    #       print('Flight event: separation')
    #     elif (field == 'F') :
    #       print('Flight event: coast start')
    #     elif (field == 'G') :
    #       print('Flight event: apogee')
    #     elif (field == 'H') :
    #       print('Flight event: coast end')
    #     elif (field == 'I') :
    #       print('Flight event: drogue chutes')
    #     elif (field == 'J') :
    #       print('Flight event: main chutes')
    #     elif (field == 'K') :
    #       print('Flight event: touchdown')
    #     elif (field == 'L') :
    #       print('Flight event: safing')
    #     elif (field == 'M') :
    #       print('Flight event: mission end')
    #     else :
    #       print('Flight event: unknown')
    #   elif (counter == 2) :
    #     print ('Experiment time: ' + field + ' sec')
    #   elif (counter == 3) :
    #     print ('Altitude: ' + field + ' ft')
    #   elif (counter == 4):
    #     print ('GPS altitude: ' + field + ' ft')
    #   elif (counter == 5):
    #     print ('Velocity:')
    #     print ('   Up: ' + field + ' ft/sec')
    #   elif (counter == 6):
    #     print ('   East: ' + field + ' ft/sec')
    #   elif (counter == 7):
    #     print ('   North: ' + field + ' ft/sec')
    #   elif (counter == 8):
    #     print ('Acceleration:')
    #     print ('   magnitude: ' + field + ' ft/sec^2')
    #   elif (counter == 9):
    #     print ('   x-axis: ' + field + ' ft/sec^2')
    #   elif (counter == 10):
    #     print ('   y-axis: ' + field + ' ft/sec^2')
    #   elif (counter == 11):
    #     print ('   z-axis: ' + field + ' ft/sec^2')
    #   elif (counter == 12):
    #     print ('Attitude:')
    #     print ('   phi: ' + field + ' radians')
    #   elif (counter == 13):
    #     print ('   theta: ' + field + ' radians')
    #   elif (counter == 14):
    #     print ('   psi: ' + field + ' radians')
    #   elif (counter == 15):
    #     print ('Angular velocity:')
    #     print ('   x-axis: ' + field + ' radians/sec')
    #   elif (counter == 16):
    #     print ('   y-axis: ' + field + ' radians/sec')
    #   elif (counter == 17):
    #     print ('   z-axis: ' + field + ' radians/sec')
    #   elif (counter == 18):
    #     if (field == '1') :
    #       print ('Liftoff Imminent warning:       true')
    #     else :
    #       print ('Liftoff Imminent warning:       false')
    #   elif (counter == 19):
    #     if (field == '1') :
    #       print ('Drogue Chute Imminent warning:  true')
    #     else :
    #       print ('Drogue Chute Imminent warning:  false')
    #   elif (counter == 20):
    #     if (field == '1') :
    #       print ('Landing Imminent warning:       true')
    #     else :
    #       print ('Landing Imminent warning:       false')
    #   elif (counter == 21):
    #     if (field == '1') :
    #       print ('Chute Fault warning:            true')
    #     else :
    #       print ('Chute Fault warning:            false')

    #   counter += 1


    # display how far along simulation is
    self.ui.nff_sim_progress_bar.setValue(100 * self.packet_counter / self.num_lines)

    # Send the packet to each connected device.
    self.publish_socket.send_string(packet)

    # Increment the packet counter.
    self.packet_counter += 1

    # Delay is chosen to result in a send rate of roughly 10Hz, call isn't very precise at ms level.
    time.sleep(0.07)

  
  def stop(self):
    self.Active = False
    print("abort sim")
    self.quit()