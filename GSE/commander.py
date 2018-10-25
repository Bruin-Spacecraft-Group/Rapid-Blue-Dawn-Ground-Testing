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
        self.response_socket = context.socket(zmq.SUB)
        self.response_socket.connect(config.COMMANDER_SUBSCRIBE)

    def command(self):
        while True:
            inputString = input("Please submit a command: ")
            try:
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
                    if args[1] != None:
                        print("setting timer for {} seconds".format(args[1]))
                        commandString += args[1]
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
                    pin = int(args[1])
                    if pin >= 0 and pin <= 13:
                        commandString += hex(pin) 
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
                elif command == 'getTelemetry':
                    commandString += 'q'
                #readPin digital/analog pin#
                elif command == "readPin":
                    commandString += "q"
                    pin = int(args[2])
                    if args[1] == "digital":
                        commandString += "d"
                        if pin >= 0 and pin <= 13:
                            commandString += hex(int(args[2])) 
                            print("reading {} pin {}".format(args[1], args[2]))
                        else:
                            print("please provide a valid pin (0-13)")
                            return
                    elif args[1] == "analog":
                        commandString += "a"
                        if pin >= 0 and pin <= 5:
                            commandString += hex(int(args[1])) 
                            print("reading {} pin {}".format(args[1], args[2]))
                        else:
                            print("please provide a valid pin (0-5)")
                            return
                    else:
                        print("please provide a valid pin type (digital/analog)")
                elif command == "testSD":
                    commandString += "d"
                    print("test SD")
                    # if args[1] == "readWrite":
                    #     commandString += "r"
                    # elif args[1] == "cardInfo":
                    #     commandString += "i"
                    # elif args[1] == "listFiles":
                    #     commandString += "f"
                    # else:
                    #     print("please provide a valid specifier (readWrite/cardInfo/listFiles")
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
            except:
                print("error parsing command {}".format(inputString))
            #send command to serial manager
            self.output_socket.send_string(commandString) 

            # while True:
            #     print("looping")
            #     response = self.response_socket.recv_pyobj()
            #     if response[0] == 'response':
            #         print(response[1])
            #         break
            #     else:
            #         continue
            # response = self.response_socket.recv_pyobj()
            # if response[0] == 'response':
            #     print("commander received response")
            #     print(response[1])

if __name__ == '__main__':
    commander = Commander()
    commander.command()