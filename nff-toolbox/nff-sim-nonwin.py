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
import curses
from curses import panel


PROGRESS_BAR_LENGTH = 80
PACKET_INTERVAL = 0.1
MAXBUFFER = 200
TIMEOUT = 0.02
BAUDRATE=115200
NUMDATAFIELDS = 25


def display_welcome_msg(win):
  win.addstr(1, 1, '****************************************')
  win.addstr(2, 1, '**    Welcome to the NFF simulator    **')
  win.addstr(3, 1, '**            NanoRacks LLC           **')
  win.addstr(4, 1, '**     Consult the ReadMe.md for      **')
  win.addstr(5, 1, '**           use instructions         **')
  win.addstr(6, 1, '****************************************') 


def print_packet(nff_win, flow_win, ada_win, in_packet):

  fields = in_packet.split(',')

  if(len(fields) != NUMDATAFIELDS):
    return

  nff_win_fields = []
  flow_win_fields = []
  ada_win_fields = []

  # Begin Time
  flow_win_fields.append(fields[0])

  # nff data
  for i in range(1, 22):
    nff_win_fields.append(fields[i])

  # flowmeter
  flow_win_fields.append(fields[22])

  # mosfet
  flow_win_fields.append(fields[23])

  # end time
  flow_win_fields.append(fields[24])

  # Print to windows
  print_flow_to_win(flow_win, flow_win_fields)
  print_nff_to_win(nff_win, nff_win_fields)


def print_flow_to_win(flow_win, flow_win_fields):

  flow_win.addstr(1, 1, "Packet Start Time: {} ms".format(flow_win_fields[0]))
  flow_win.addstr(2, 1, "Packet End Time: {} ms".format(flow_win_fields[3]))

  flow_win.addstr(4, 1, "Mosfet switch: {}".format(flow_win_fields[1]))
  flow_win.addstr(6, 1, "Flowrate: {} m/s".format(flow_win_fields[2]))




def print_nff_to_win(nff_win, nff_win_fields):

    # Split line input from the arduino
    # Print all of the flight information in an easy to read format
    counter = 1
    for field in nff_win_fields :
      if (counter == 1) :
        if (field == '@') :
          nff_win.addstr(1, 1, 'Flight state: none reached')
        elif (field == 'A') :
          nff_win.addstr(1, 1, 'Flight state: liftoff')
        elif (field == 'B') :
          nff_win.addstr(1, 1, 'Flight state: meco')
        elif (field == 'C') :
          nff_win.addstr(1, 1, 'Flight state: separation')
        elif (field == 'D') :
          nff_win.addstr(1, 1, 'Flight state: coast_start')
        elif (field == 'E') :
          nff_win.addstr(1, 1, 'Flight state: apogee')
        elif (field == 'F') :
          nff_win.addstr(1, 1, 'Flight state: coast_end')
        elif (field == 'G') :
          nff_win.addstr(1, 1, 'Flight state: under_chutes')
        elif (field == 'H') :
          nff_win.addstr(1, 1, 'Flight state: landing')
        elif (field == 'I') :
          nff_win.addstr(1, 1, 'Flight state: safing')
        elif (field == 'J') :
          nff_win.addstr(1, 1, 'Flight state: finished')
        else :
          nff_win.addstr(1, 1, 'Flight state: unknown')
      elif (counter == 2) :
        nff_win.addstr(2, 1, 'Experiment time: ' + field + ' sec')
      elif (counter == 3) :
        nff_win.addstr(3, 1, 'Altitude: ' + field + ' ft')
      elif (counter == 4):
        nff_win.addstr(4, 1, 'Velocity:')
        nff_win.addstr(5, 1, '   x-axis: ' + field + ' ft/sec')
      elif (counter == 5):
        nff_win.addstr(6, 1, '   y-axis: ' + field + ' ft/sec')
      elif (counter == 6):
        nff_win.addstr(7, 1, '   z-axis: ' + field + ' ft/sec')
      elif (counter == 7):
        nff_win.addstr(8, 1, 'Acceleration:')
        nff_win.addstr(9, 1, '   magnitude: ' + field + ' ft/sec^2')
      elif (counter == 8):
        nff_win.addstr(10, 1, '   not-used: ' + field)
      elif (counter == 9):
        nff_win.addstr(11, 1, '   not-used: ' + field)
      elif (counter == 10):
        nff_win.addstr(12, 1, 'Attitude:')
        nff_win.addstr(13, 1, '   x-axis: ' + field + ' radians')
      elif (counter == 11):
        nff_win.addstr(14, 1, '   y-axis: ' + field + ' radians')
      elif (counter == 12):
        nff_win.addstr(15, 1, '   z-axis: ' + field + ' radians')
      elif (counter == 13):
        nff_win.addstr(16, 1, 'Angular velocity:')
        nff_win.addstr(17, 1, '   x-axis: ' + field + ' radians/sec')
      elif (counter == 14):
        nff_win.addstr(18, 1, '   y-axis: ' + field + ' radians/sec')
      elif (counter == 15):
        nff_win.addstr(19, 1, '   z-axis: ' + field + ' radians/sec')
      elif (counter == 16):
        if (field == '1') :
          nff_win.addstr(20, 1, 'Liftoff warning: true')
        else :
          nff_win.addstr(20, 1, 'Liftoff warning: false')
      elif (counter == 17):
        if (field == '1') :
          nff_win.addstr(21, 1, 'RCS warning:     true')
        else :
          nff_win.addstr(21, 1, 'RCS warning:     false')
      elif (counter == 18):
        if (field == '1') :
          nff_win.addstr(22, 1, 'Escape warning:  true')
        else :
          nff_win.addstr(22, 1, 'Escape warning:  false')
      elif (counter == 19):
        if (field == '1') :
          nff_win.addstr(23, 1, 'Chute warning:   true')
        else :
          nff_win.addstr(23, 1, 'Chute warning:   false')
      elif (counter == 20):
        if (field == '1') :
          nff_win.addstr(24, 1, 'Landing warning: true')
        else :
          nff_win.addstr(24, 1, 'Landing warning: false')
      elif (counter == 21):
        if (field == '1') :
          nff_win.addstr(25, 1, 'Fault warning:   true')
        else :
          nff_win.addstr(25, 1, 'Fault warning:   false')

      counter += 1



def main(stdscr):

  # Array for holding serial connections.
  ser = []

  # Clear screen
  stdscr.clear()

  # Get screen dimensions
  scr_height, scr_width = stdscr.getmaxyx()

  # Create welcome window and panel
  welcome_win = curses.newwin(scr_height, scr_width, 0, 0)
  welcome_panel = panel.new_panel(welcome_win)

  # Display welcome message.
  display_welcome_msg(welcome_win)

  # Prompt user for the com ports to connect to.

  # Echo characters to user
  curses.echo()

  welcome_win.addstr(8, 1, 'Enter the ports to connect to: ')
  
  # Show panels
  panel.update_panels()
  curses.doupdate()

  myinput = welcome_win.getstr(9, 1).decode(encoding="utf-8")

  welcome_win.addstr('\n')

  # Try to connect to each of the com ports provided by the user. If the
  # connection was successful then add it to the array of serial connections.
  for port in myinput.split() :
    try :
      temp = serial.Serial(port=port, baudrate=BAUDRATE, timeout=TIMEOUT)
      ser.append(temp)
      welcome_win.addstr('Successfully connected to: ' + port + '\n')
    
    except :
      welcome_win.addstr('Failed to connect to: ' + port + '\n')
  
  # Show panels
  panel.update_panels()
  curses.doupdate()

  # If no connections are made then tell the user and exit the program.
  if len(ser) == 0 :
    welcome_win.addstr('Error: no connections established\n')
    welcome_win.addstr('Check the com port and ensure no other programs are connected to it\n\n')
    welcome_win.addstr('Press <enter> to exit\n')

    # Update panels
    panel.update_panels()
    curses.doupdate()

    discard = stdscr.getch() # block
    return

  # Try to open the text file with all of the packets to send and exit
  # if it fails to open.
  try:
    infile = open('nff-packets.txt', 'r')

  except:
    welcome_win.addstr('Error: couldn\'t open nff-packets.txt\n')
    welcome_win.addstr('Make sure the file is in the same directory as the .exe\n\n')
    welcome_win.addstr('Press <enter> to exit\n')

    # Update panels
    panel.update_panels()
    curses.doupdate()

    discard = stdscr.getch() # block
    return


  # Try and open output file
  try:
    timestr = time.strftime("%d-%b-%Y_%H:%M:%S", time.localtime())
    outfile = open("log/" + timestr + "_log.txt",  "w+")

  except:
    welcome_win.addstr('Error: couldn\'t open logfile\n\n')
    welcome_win.addstr('Press <enter> to exit\n')

    # Update panels
    panel.update_panels()
    curses.doupdate()

    discard = stdscr.getch() # block
    return

  # Make sure files are open
  time.sleep(0.1)

  # Wait until user is ready to start the simulation.
  welcome_win.addstr('Press <enter> to start the simulation!\n')

  # Update panels
  panel.update_panels()
  curses.doupdate()

  discard = stdscr.getch() # block
  

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
  packets_sent = 0


  # Init windows for testing

  '''
  header_win is for storing raw data sent and received

  nff_win is for nff packets received
  flow_win is for flowmeter data
  ada_win is for the data received from adafruit sensor

  foot_win is progress bar and cmd list

  '''
  del welcome_win

  header_win  = curses.newwin(13, scr_width,            0,    0)
  nff_win     = curses.newwin(27, int(scr_width/3)-1,   13,   0)
  flow_win    = curses.newwin(27, int(scr_width/3)-1,   13,   int(scr_width/3))
  ada_win     = curses.newwin(27, int(scr_width/3)-1,   13,   int(scr_width/3)*2)
  foot_win    = curses.newwin(10,  scr_width,           40,   0)

  header_panel = panel.new_panel(header_win)
  nff_panel    = panel.new_panel(nff_win)
  flow_panel   = panel.new_panel(flow_win)
  ada_panel    = panel.new_panel(ada_win)
  foot_panel   = panel.new_panel(foot_win)

  panel.update_panels()
  curses.doupdate()

  # Turn off echo mode and make keypresses nonblocking
  curses.noecho()
  stdscr.nodelay(True)

  # Main Loop

  while True:

    # Clear windows
    header_win.erase()
    nff_win.erase()
    flow_win.erase()
    ada_win.erase()
    foot_win.erase()

    # Borders look organized and cool
    header_win.border()
    nff_win.border()
    flow_win.border()
    ada_win.border()
    foot_win.border()


    # Send packet if time interval is met
    curr_time = datetime.datetime.utcnow().timestamp()
    if curr_time - prev_time > PACKET_INTERVAL and packet_counter < num_lines:

      line = all_lines[packet_counter]
      packet = line.rstrip()

      # Send the packet to each connected device.
      for devs in ser :
        devs.write(packet.encode())

      out_packet = line
      prev_time = curr_time
      packet_counter += speed
      packets_sent += 1


    # Check for keystroke input from user
    c = stdscr.getch()

    if(c == ord('q')):
      # (q)uit
      break
    elif(c == ord('p')):
      # (p)ause
      stdscr.nodelay(False)
      discard = stdscr.getch() # Wait for p to be pressed again
      stdscr.nodelay(True)
    elif(c == curses.KEY_LEFT and speed != 1):
      # Slow down! Left key pressed
      speed = int(speed / 2)
    elif(c == curses.KEY_RIGHT and speed != 64):
      # Speed up! Right key pressed
      speed = int(speed * 2)


    # Listen for response from Arduino

    # Read in up to the maximum size of data per line.
    # 0 is used because we only have 1 arduinp
    data_in = ser[0].readline(MAXBUFFER).decode()
    # ser[0].reset_input_buffer()

    # Strip newline characters
    data_in = data_in.rstrip('\n')
    data_in = data_in.rstrip('\r')
    data_in = data_in.rstrip('\n')

    # Check that some data was received.
    if (len(data_in) != 0):
      in_packet = data_in

    # Verify size of packet received
    if(len(data_in.split(",")) == NUMDATAFIELDS):
      packets_received += 1

    # Output contents to logfile
    outfile.write(in_packet + "\n")

    # Cool running effect with the dots.
    header_win.addstr(1, 1, 'NFF simulation running' + ('.' * (int)((packet_counter % 12) / 3)))

    # Display all of the connected ports.
    ports = ""
    for devs in ser:
      ports += devs.port + ", "

    header_win.addstr(3, 1, 'Connected to: ' + ports[:-2])

    # Display the current packet being sent.
    header_win.addstr(5, 1, 'Sending packet: ' + out_packet)

    # Print packet received from arduino
    header_win.addstr(7, 1, "Packet received: " + in_packet)
    header_win.addstr(8, 1, "Length: {}".format(len(in_packet.split(","))))

    # Companre number of packets received to packets sent
    header_win.addstr(10, 1, "Packets sent: {}".format(packets_sent))
    header_win.addstr(11, 1, "Packets received: {}".format(packets_received))

    # Print contents of packet to console
    print_packet(nff_win, flow_win, ada_win, in_packet)

    # Temp
    ada_win.addstr(1, 1, "Adafruit 9-DOF Sensor")

       
    # Display how far along the simulation is with a neat loading bar (the magic 20 number is to
    # prevent the simulation from obnoxiously ending while displaying 99%, I'm a little OCD).
    foot_win.addstr(1, 1, 'Simulation progress: [' + '#' * (int)(packet_counter / (num_lines / PROGRESS_BAR_LENGTH)) 
          + ' ' * (int)(PROGRESS_BAR_LENGTH - (packet_counter / (num_lines / PROGRESS_BAR_LENGTH))) + '] ' 
          + str(((100 * (int)(packet_counter + 20)) / num_lines)) + '%')
    

    # Display the current speed the simulation is running at.
    foot_win.addstr(3, 1,'Current speed: x' + str(speed))
    foot_win.addstr(4, 1,'Press left to slow down sim or right to speed up sim')

    # Inform user about option to quit
    foot_win.addstr(6, 1,'Press <q> at any time to quit or <p> to pause')

    panel.update_panels()
    curses.doupdate()

    time.sleep(0.02)


  # Close all device connections after simulation has finished.
  for devs in ser :
    devs.close()

  # Close files
  infile.close()
  outfile.close()


curses.wrapper(main)