# Feather Frame Simulator

```
                                         |
                                         |
                                         |
                                         |
   _______        NFF        ________    |
  |ooooooo|      ____       | __  __ |   |
  |[]+++[]|     [____]      |/  \/  \|   |
  |+ ___ +|     ]()()[      |\__/\__/|   |
  |:|   |:|   ___\__/___    |[][][][]|   |
  |:|___|:|  |__|    |__|   |++++++++|   |
  |[]===[]|   |_|_/\_|_|    | ______ |   |
_ ||||||||| _ | | __ | | __ ||______|| __|
  |_______|   |_|[::]|_|    |________|   \
              \_|_||_|_/                  \
                |_||_|                     \
               _|_||_|_                     \
 Troy ____    |___||___|                     \
     /  __\          ____                     \
     \( oo          (___ \                     \
     _\_o/           oo~)/  Zach
    / \|/ \         _\-_/_
   / / __\ \___    / \|/  \
   \ \|   |__/_)  / / .- \ \
    \/_)  |       \ \ .  /_/
     ||___|        \/___(_/
     | | |          | |  |
     | | |          | |  |
     |_|_|          |_|__|
     [__)_)        (_(___]
```

## Instructions
The nff-sim program is designed to assist in the testing and development of feather frame payloads. The program connects to one or more serial devices that are provided by the user and then waits for the user to start the simulation. A simulation consists of the feather frame program reading in data packets from an included file `nff-packets.txt` and sending these data packets to all of the connected devices at appx 10Hz to mimic the functionality of the actual feather frame. The data packets used in the simulation are derived from actual flight data provided by Blue Origin that represent a nominal flight. During the simulation a list of connected devices is displayed along with the current data packet that is being sent and a status bar to show the progress of the simulation. The simulation can be stopped at any time by pressing **`q`** for quit and otherwise will run until the simulation finishes sending all of the packets.


## Requirements
+ The nff-sim.exe program is a Windows 32-bit executable and should work on any Windows OS. If the .exe doesn't work then you can run the python program instead, keeping in mind that the pyserial library will need to be installed in order for it to work.
+ The program needs the name of a serial port that has no other programs connected to it, which
    it will then connect to and send the serial packets.

## Usage
Using the nff-sim is fairly straightforward:

1. Check that the `nff-sim.exe` and `nff-packets.txt` files are located in the same folder.
2. Connect your feather frame payload to your computer with a handy-dandy USB cable (2.0 or 3.0).
3. Check what `COM` port your payload shows up as on the computer. This can typically be found by looking under `Device Manager->Ports(COM & LPT)` and will often show up as something like `USB Serial Port (COM7)`. The port name you would provide to the program in this case would be the name in the parentheses: `COM7`.
4. Double click the executable file nff-sim.exe to run it and you should see a welcome message that says `Welcome to the NFF simulator` and a note telling you to consult the readme.
5. The program will then prompt you to enter the ports you would like to connect to. Simply enter in the name of the ports (with spaces in between each entry if there are multiple). For our example, you would simply type COM7 and then press enter.
6. After entering the ports the program will try to connect to each one and print either `successfully connected to port` or `failed to successfully connect to port` for each of the ports that were provided. (For reasons why connection to a port might fail consult the troubleshooting section of the readme).
7. Once all the connections are displayed, the program will prompt the user to press enter to start the simulation. Make sure that the experiment is completely ready for testing and then press enter to begin.
8. After the simulation has started, the program will send data packets to the payload at approximately 10Hz (up to 0.4Hz variation was seen during testing), for a description of these data packets reference the packet description section of the readme.
9. As the simulation is running, the program will display several messages:
  * A note that the simulation is active.
  * A list of the connected ports.
  * The current packet being sent by the simulation.
  * The current flight information contained in the packet.
  * The progress of the simulation shown graphically by a status bar.
  * A note that pressing **`q`** will quit the simulation.
10. Once the simulation has finished sending all of the data packets, or after the user has quit the simulation, a message will appear that informs the user that the simulation was completed along with a prompt to press <enter> to exit. At this point simply press enter and the program will exit.
11. Pat yourself on the back for successfully using the nff-sim! (Or consult the troubleshooting section if you were less successful.)

## Troubleshooting
Using the program should be very simple and straightforward for most users, but there are a couple very common mistakes that could lead to some unexpected behavior and possibly cause some headaches:

1. `Error: no connections established` - 
This error is caused by a failure to connect to the user provided ports, and the recommended steps for fixing this issue are:
  * Make sure the provided port is the correct port that your device is connected to, and that if you entered multiple ports they were separated only by spaces. The easisest way to double check the port your device is on is to pull up device manager in Windows and look under `Ports (COM & LPT)` for the port your device is on. Unplug your device and then plug it back in, and you should notice the port name disappear from the list and then reappear.
  * Check that no other program is connected to that port. Only one program can connect to a given serial  port at a time, so if you have putty or some other program connected to a port then the nff-sim will  be unable to establish a connection. Sometime programs that you thought are closed are still running in the background and so pull up the task manager on Windows `ctrl+alt+del` and look to see if any programs may still be running that are connected to the device.
  * Run the program as an administrator. This has not been necessary in any testing, but depending on the security settings it's possible that on some systems the program will need to be run as admin to be able to access the serial ports.

2. `Error: couldn't open nff-packets.txt` - 
This error occurs when the nff-sim.exe is run in a different directory than where the nff-packets.txt is kept. 
  * Simply keep all the nff-sim files in one folder and this error should be avoided. 
  * If the text file is in the same directory then check the file properties and make sure that it can be opened for reading by a normal text editor.

3. `No error but strange behavior` - 
The nff-sim continually sends data by reading from the nff-packets.txt file, so any modification to the text file will result in unexpected data being sent by the simulator and should be avoided. Also, there are slight variations in timing as the code uses the Windows OS sleep function for its timing, but these shouldn't be large enough to impact the performance of payloads. The data will nominally be sent at 10Hz, but it can vary by as much as 0.5 Hz. 
  * Any other unexpected issues should be reported to NanoRacks LLC and we'll do our best to sort out any problems as quick as possible.


## Packet Description
The data packets sent by the nff-sim are long strings of no more than 200 bytes that contain 21 different data fields separated by commas with no data field exceeding 20 bytes in length. The data is sent serially at a baud rate of 115200 with 8 data bits, no parity, and 1 stop bit `8N1`. This data configuration should be the default for almost all microcontrollers and serial devices unless specified otherwise. 

The data fields are ordered as follows:

1. `Current flight state` - this will be represented as a single character and the chart below shows each flight state with their corresponding character.

| Flight state  | Character |
| ------------- | --------- |
|  None         |     @     |
|  Liftoff      |     A     |
|  Meco         |     B     |
|  Separation   |     C     |
|  Coast_Start  |     D     |
|  Apogee       |     E     |
|  Coast_End    |     F     |
|  Under_Chutes |     G     |
|  Landing      |     H     |
|  Safing       |     I     |
|  Finished     |     J     |

2. `Experiment time` - the current experiment time as a decimal number with 2 digits after the decimal point.

3. `Altitude` - the current altitude above ground level as a decimal number with 6 digits after the decimal point.

4. `Velocity x-axis` - the current x-axis (x-axis is directed away from the ground) velocity in feet per second as a decimal number with 6 digits after the decimal point.

5. `Velocity y-axis` - the current y-axis (y-axis faces East) velocity in feet per second as a decimal number with 6 digits after the decimal point.

6. `Velocity z-axis` - the current z-axis (z-axis faces North) velocity in feet per second as a decimal number with 6 digits after the decimal point.

7. `Acceleration` - the magnitude of the current acceleration in feet per second squared as a decimal number with 6 digits after the decimal point.

8. `Not used` - This field is reserved for future use, but is currently a constant zero valued decimal number with 6 digits after the decimal point.

9. `Not used` - This field is reserved for future use, but is currently a constant zero valued decimal number with 6 digits after the decimal point.

10. `Attitude x-axis` - the current attitude about the x-axis in radians as a decimal number with 6 digits after the decimal point.

11. `Attitude y-axis` - the current attitude about the y-axis in radians as a decimal number with 6 digits after the decimal point.

12. `Attitude z-axis` - the current attitude about the z-axis in radians as a decimal number with 6 digits after the decimal point.

13. `Angular velocity x-axis` - the current angular velocity about the x-axis in radians per second as a decimal number with 6 digits after the decimal point.

14. `Angular velocity y-axis` - the current angular velocity about the y-axis in radians per second as a decimal number with 6 digits after the decimal point.

15. `Angular velocity z-axis` - the current angular velocity about the z-axis in radians per second as a decimal number with 6 digits after the decimal point.

16. `Liftoff warning` - warning triggered on main engine ignition, value is a single digit with a 1 when the warning is true and 0 when it is false.

17. `RCS warning` - warning triggered during microgravity phase of flight to notify that attitude adjustments are in progress, value is a single digit with a 1 when the warning is true and 0 when it is false.

18. `Escape warning` - warning triggered during the escape motor ignition process, value is a single digit with a 1 when the warning is true and 0 when it is false.

19. `Chute warning` - warning triggered shortly before drogue chute deployments, value is a single digit with a 1 when the warning is true and 0 when it is false.

20. `Landing warning` - warning triggered by altitude shortly before the crew capsule touches down, value is a single digit with a 1 when the warning is true and 0 when it is false.

21. `Fault warning` - warning triggered in anticipation of an abnormally hard landing, value is a single digit with a 1 when the warning is true and 0 when it is false.

An example data packet would be:
`G,496.56,9697.791016,-216.117355,0.239193,-0.373560,32.779297,0.000000,0.000000,-0.272123,-0.004113,0.000209,-0.001000,0.000000,0.000000,0,0,0,1,0,0`

Looking at the fields we can discern that:

```
Flight state    = Under_Chutes (G)
Experiment time = 496.56 sec
Altitude        = 9697.791016 ft
Velocity:
  x-axis        = -216.117355 ft/sec
  y-axis        = 0.239193 ft/sec
  z-axis        = -0.373560 ft/sec
Acceleration:
  magnitude     = 32.779297 ft/sec^2
  n/a           = 0.000000 ft/sec^2
  n/a           = 0.000000 ft/sec^2
Attitude: 
  x-axis        = -0.272123 radians
  y-axis        = -0.004113 radians
  z-axis        = 0.000209 radians
Angular velocity:
  x-axis        = -0.001000 radians/sec
  y-axis        = 0.000000 radians/sec
  z-axis        = 0.000000 radians/sec
Liftoff warning = false
RCS warning     = false
Escape warning  = false
Chute warning   = true
Landing warning = false
Fault warning   = false
```

For any further questions about the nff-sim please contact NanoRacks LLC and we will try to answer your questions
as quickly as possible. Happy developing!
