README.md

Setup:

For Windows: 
- Locate the port at which the Arduino is connected to the computer. 
- Run the executable located in nff-toobox/Simulator, which should start simulating the data packets from NFF.

For Mac and Linux:
- Locate the port at which the Arduino is connected to the computer. This can be found by looking under Tools/Ports in the Arduino IDE, or running "ls /dev/tty.usb*" in the Terminal
- Run the simulator (nff-sim-nonwin.py) using Python3, i.e. "python3 nff-sim-nonwin.py"

Note that controls for both are slightly different, speed up and down for Mac and Linux is mapped to different keys.