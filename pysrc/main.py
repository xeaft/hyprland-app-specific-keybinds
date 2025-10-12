import threading
import socket_listener
import conf_parser
import argparse
import importlib.util

def is_module(mod : str) -> bool:
    return importlib.util.find_spec(mod) is not None

def try_start_inotify_proc() -> None:
    if not is_module("pyinotify"):
        print("pyinotify not found, cant watch inotify")
        return
    watcher = __import__("inotify_watcher")
    print("started watcher")
    watcher.register_watcher()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="hyprwinbinds", description="allows you to set keybinds for specific window classes", usage="%(prog)s [keyword?] [options?]")
    
    parser.add_argument("-l", "--show-logs", action="store_true")
    parser.add_help = True
    
    args = parser.parse_args()

    config = conf_parser.read_keybinds_file()
    keys = conf_parser.parse_key_lines(config)

    thread = threading.Thread(target=try_start_inotify_proc, daemon=True)
    thread.start()
    socket = socket_listener.create_socket(keys, args.show_logs)

