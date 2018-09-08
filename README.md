Blue Dawn Ground Testing
=========================  
# Project Rapid

## About:

### Welcome to the Rapid's repository for our Ground Testing Software suite.
The main item of interest is the GSE software. 
Second is the code to be run on the Flight Computer in it's test configuration. 
Also included is the code to be run on the custom umbilical cable which serves to measure the voltage and current draw of the Blue Dawn vehicle.
We hav eincluded the nff-toolbox for ease of access and integration with our suite, though it is the property of Nanoracks LLC.
Finally there are antiquated test scripts currently kept for no real reason.

## Requirements
This software is designed to be cross-platform compatible. 
- It is built using `Python 3`, `PyQt5`, and `Arduino`.
Python packages can be installed using `pip`. 
- From the root project directory, run the command `pip install -r requirements.txt`. 
We reccommend doing so in a python virtual environment in order to ensure stability.

If you do not have the Aruino IDE installed, do so now.

## Setup
### Flight Computer
- Connect the Flight Computer to the Umbilical, ensure the umbilical is switched OFF. 
- Connect both USB A cables (P2 and P3) from the Umbilical to your computer.
- Open the Arduino IDE and note which port is being used by the the Umbilical's Nano and which by the Flight Computer's Uno. 
- Upload `CurrentSenseUmbilical.ino` to the Umbilical's Nano (via P2).
     - Check the Serial Monitor at 115200 to ensure telemetry is printing to the serial port.
- Upload `Blue_Dawn_Test_Config.ino` to the Flight Computer (via P3).
     - Check the Serial Monitor at 115200 to ensure telemetry is printing to the serial port.
- Close the Serial Monitor.

### GSE
See `GSE/README.md`.
