import logging
import threading
import socket_listener
import conf_parser
import argparse
import importlib.util
from glog import logger
from hyprvarparser import get_vars_from_file
from hyprvar import HyprVar
from typing import List

def is_module(mod : str) -> bool:
    return importlib.util.find_spec(mod) is not None

def try_start_inotify_proc() -> None:
    if not is_module("pyinotify"):
        logger.warning("pyinotify not found, cant watch inotify")
        return
    watcher = __import__("inotify_watcher")
    logger.info("started watcher")
    watcher.register_watcher()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="hyprwinbinds", description="allows you to set keybinds for specific window classes", usage="%(prog)s [keyword?] [options?]")
    
    parser.add_argument("-l", "--show-logs", action="store_true")
    parser.add_help = True
    
    args = parser.parse_args()
    
    if args.show_logs:
        logger.setLevel(logging.DEBUG)

    conf_file = conf_parser.get_conf_file_loc()

    hyprvars : List[HyprVar] = get_vars_from_file(conf_file)

    config = conf_parser.read_keybinds_file(conf_file)
    keys = conf_parser.parse_key_lines(config, hyprvars)

    thread = threading.Thread(target=try_start_inotify_proc, daemon=True)
    thread.start()
    socket = socket_listener.create_socket(keys)

