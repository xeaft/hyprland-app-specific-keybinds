import sys
import socket_listener
import conf_parser
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="hyprwinbinds", description="allows you to set keybinds for specific window classes", usage="%(prog)s [keyword?] [options?]")
    
    parser.add_argument("-l", "--show-logs", action="store_true")
    parser.add_help = True
    
    args = parser.parse_args()

    config = conf_parser.read_keybinds_file()
    keys = conf_parser.parse_key_lines(config)
    socket = socket_listener.create_socket(keys, args.show_logs)

