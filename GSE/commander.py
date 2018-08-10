import zmq
import datetime
import sys
import config 
import argparse

class Commander:
    def __init__(self):
        context = zmq.Context()
        self.output_socket = context.socket(zmq.PUB)
        self.output_socket.bind(config.COMMANDER_PUBLISH)
    
    def command(self):
        while True:
            inputString = input("Please submit a command: ")
            args = inputString.split(" ")
            command = args[0]
            #start character for gse commands
            #used for flight computer's parsing
            commandString = "c"

            #ping
            if command == "ping":
                commandString += "p"
                print("pinging flight computer")
            #mosfet ENABLE/DISABLE
            elif command == "mosfet":
                commandString += "m"
                if args[1] == "ENABLE":
                    print("enabling electrodes")
                    commandString += "1"
                elif args[1] == "DISABLE":
                    print("disabling electrodes")
                    commandString += "0"
                else:
                    print("please provide a valid mosfet state (ENABLE/DISABLE)")
                    return
            #timer value [in seconds]
            elif command == "timer":
                commandString += "t"
                if args[1] != None and args[1] > 0:
                    print("setting timer for {} seconds".format(args[1]))
                    commandString += str(args[1])
                else:
                    print("please provide a valid timer duration")
                    return
            #reset
            elif command == "reset":
                commandString += "r"
                print("resetting")
            #setPin pin# HIGH/LOW
            elif command == "setPin":
                commandString += "s"
                if args[1] >= 0 and args[1] <= 13:
                    commandString += hex(int(args[1])) 
                    if args[2] == "HIGH":
                        commandString += "h"
                        print("setting pin {} HIGH".format(args[1]))
                    elif args[2] == "LOW":
                        commandString += "l"
                        print("setting pin {} LOW".format(args[1]))
                    else:
                        print("please input valid pin state (HIGH/LOW)")
                        return
                else:
                    print("please provide a valid pin (0-13)")
                    return
            #readPin digital/analog pin#
            elif command == "readPin":
                commandString += "p"
                if args[1] == "digital":
                    commandString += "d"
                    if args[2] >= 0 and args[2] <= 13:
                        commandString += hex(int(args[2])) 
                        print("reading {} pin {}".format(args[1], args[2]))
                    else:
                        print("please provide a valid pin (0-13)")
                        return
                elif args[1] == "analog":
                    commandString += "a"
                    if args[2] >= 0 and args[2] <= 5:
                        commandString += hex(int(args[1])) 
                        print("reading {} pin {}".format(args[1], args[2]))
                    else:
                        print("please provide a valid pin (0-5)")
                        return
                else:
                    print("please provide a valid pin type (digital/analog)")
            elif command == "testSD":
                commandString += "d"
                if args[1] == "readWrite":
                    commandString += "r"
                elif args[1] == "cardInfo":
                    commandString += "i"
                elif args[1] == "listFiles":
                    commandString += "f"
                else:
                    print("please provide a valid specifier (readWrite/cardInfo/listFiles")
            #TODO
            elif command == "writeToSD":
                print("How about you try a command we actually like? We don't support this one.")
                return
            #TODO
            elif command == "readFromSD":
                print("How about you try a command we actually like? We don't support this one.")
                return
            #sendNFFPacket
            elif command == "sendNFFPacket":
                print("How about you try a command we actually like? We don't support this one.")
                return
            else:
                print('bad command "{}"'.format(command))

            #send command to serial manager
            self.output_socket.send_string(commandString) 

if __name__ == '__main__':
    commander = Commander()
    commander.command()