import socket_listener
import conf_parser
import threading

if __name__ == "__main__":
    config = conf_parser.read_keybinds_file()
    keys = conf_parser.parse_key_lines(config)
    socket = socket_listener.create_socket(keys)

