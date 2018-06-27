README.md

Setup:

Upload the Arduino code (available in the Rapid Blue Dawn Flight library on github) to the Arduino. Do not open the Serial Monitor on the Arduino IDE!

For Mac and Linux:
- Locate the port at which the Arduino is connected to the computer. This can be found by looking under Tools/Ports in the Arduino IDE, or running "ls /dev/tty.usb*" in the Terminal
- Run the simulator (nff-sim-nonwin.py) using Python3, i.e. "python3 nff-toolbox/nff-sim-nonwin.py"

Currently unavailable for Windows, as the Curses module is only available for Mac and Linux

For Windows, download an app that makes use of Windows Subsystem for Linux, then run from there.
Notes on connecting to Arduino from WSL:
- To make sure port is free, run `sudo chmod 666 /dev/ttyS[COM port #]`
- Ensure correct baud rate: run `stty -F /dev/ttyS[COM port #] sane [Baud rate]`
- Then simply run python script, and when prompted attempt to connect to `/dev/ttyS[COM port #]`
