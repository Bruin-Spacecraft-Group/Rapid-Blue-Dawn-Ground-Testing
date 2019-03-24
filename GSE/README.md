Rapid GSE
==========
This is the beginning of Ground Support Equipment development at Bruin Space,
intended to facilitate Assembly, Integration, and Test work on any project.
Currently designed for Project Rapid's Blue Dawn mission, we hope to create a
developer friendly API that will allow future projects to easily adapt this system.

Developed on `Python 3.7`

## Getting Started
Do the thing. Download the requirements. Download more RAM.

## Using the GSE
### Setup
To begin, run `python3 main.py` from the `GSE` directory. This should initialize the gui as well as the telemetry processor server. You should see the *Main Window* appear with two text input areas for `Blue Dawn Port` and `Umbilical Port`. Input the corresponding serial ports the devices have connected to on your computer and click `Connect`.
### Monitor
After connecting to the serial ports from the *Main Window*, the *Monitor Window* should launch. This window has three main sections: _Blue Dawn_, _NFF Data_, and _Command_. _Blue Dawn_ and _NFF Data_ will automatically populate with telemetry data from Blue Dawn and the Umbilical as it comes through.
### Commander
The _Command_ section initializes an instance of IPython via Jupyter's QtConsole. This functions essentially as a terminal where you can run commands and provide user input.
To launch the *Commander* from the *Monitor Window*, run the command `%run commander`. It will then prompt you to input a command string. The syntax is as follows.
### Command Interface
Each command follows the following structure: `command specifier value`. Each field is separated by a single space. Simply press enter after supplying your command string and the commander will execute your command. You will then be prompted to run another command.
### Commands

| Input command string                   | Description                                                                                                                 | Output command string    |
|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|--------------------------|
| `ping`                                 | pings the flight computer to ensure good connection.                                                                        | `p`                        |
| `reset`                                | causes the flight computer to restart.                                                                                      | `r`                        |
| `mosfet [ENABLE/DISABLE]`              | sets the mosfet enable pin to high or low to activate/deactivate electrodes.                                                | `m1` or `m0`                 |
| `timer [value]`                        | sets a timer on the flight computer for the designated amount of time in seconds. Value must be a number greater than zero. | `t[number]`                |
| `setPin [pinNumber] [HIGH/LOW]`        | sets digital pin to HIGH or LOW                                                                                             | `s[single hex digit][h/l]` |
| `readPin [digital/analog] [pinNumber]` | reads digital or analog pin. Digital pins must be between 0-13, and analog between 0-5.                                     | `q[d/a][single hex digit]` |
| `testSD [option]`                      | make use of SD library's example test functions. Options choose from `readWrite`, `cardInfo`, and `listFiles`.              | `dr`, `di`, or `df`            |
| `sendNFFPacket`                         | sends one packet from NFF data stream to flight computer.                                                                   | `n[rest of NFF packet]`    |



## Developer Notes
===================
Current flow:
- User runs gui.py
    - this is a QMainWindow, so it's the head of everything. (Might want to rename this to like GSE.py or something)
    - It spawns an instance of SerialManager (QThread) and Server (QThread). These processes run in separate threads from the main gui
    - Note these children do not get created until after the user inputs the serial ports corresponding to the spacecraft and the umbilical respectively. 
- SerialManager
    - with the parent gui having recieved user input for the serial ports, the SerialManager initializes and opens pyserial connections
    - it then creates zmq sockets to publish data read over serial to the server, and to subscribe to command strings sent by the Commander 
    - SerialManager coordinates sending commands and reading data from the connected devices
    - Note it will hold until it recieves data from both devices to best sync information. Therefore data output rates should be identical on the connected devices 
- Server 
    - create zmq sockets subscribing to data from serial manager and publishing to the gui (technically just input and output addresses, so other processes could send data to the server via the input address that it wants disseminated over the output address, e.g. we could hook up a database process to the output address, so data that gets displayed to the gui is also saved)
    - creates instance of TelemetryProcessor to handle incoming data and format it for publishing via the output socket
    - TelemetryProcessor requires a packetmap to read input csv strings and turn them into data objects
    - Server will keep a log of data that passes through eventually, currently has support for saving to a text file, though it is disabled
- Commander
    - currently this is essentially an independent program that is run from a jupyter console window within the GSE main gui
    - takes user input in a human readable string, then converts to a few characters designated in and parsable by the flight code 
    - then it sends those few characters as a command string to the SerialManager over a zmq publish socket, which then sends the command to the appropriate device when possible






### TODO 
- update Commander command mappings
- update TelemetryProcessor data packet map
- reflect data packet updates in gui
- Spawn commander automatically - don't require user to type in %run commander.py
    - integrate commander with main gse file (gui.py currently)
- handle asynchronus data from umbilical and spacecraft
- make commander command mapping a dict in config.py, rather than hardcoded
- make window for displaying server data stream -- cannot just print to console because:
- bug where all print statements get forwarded to the jupyter window after it launches the commander script
    - might be fixed by moving commander into the main gui.py parent?