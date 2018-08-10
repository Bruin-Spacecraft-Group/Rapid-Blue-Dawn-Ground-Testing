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
