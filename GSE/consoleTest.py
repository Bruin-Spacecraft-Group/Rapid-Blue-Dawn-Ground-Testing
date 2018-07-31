import argparse
from time import sleep

def main(args):
    command = args.command
    if command == "mosfet":
        if args.value == 1:
            print("setting mosfet high")
        else:
            print("setting mosfet high")

    elif command == "timer":
        if args.value != None:
            print("setting timer for {} seconds".format(args.value))
        else:
            print("please provide a timer duration")
    elif command == "reset":
        print("resetting")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send commands to flight computer')
    parser.add_argument('command', help='a string specifying the command')
    parser.add_argument('value', help='for commands which take additional arguments, e.g. timer')

    args = parser.parse_args()
    main(args)