from logging import log
import os
import subprocess
import sys
import socket
from typing import List, NoReturn
from keybind import Keybind
import signal
import conf_parser
from window import Window
import re
from glog import logger
from hyprvarparser import get_vars_from_file

EVENT_WINDOW_FOCUSED = "activewindowv2"

app_keybinds = []
current_window : Window|None = None
running = True
sock = None

bool_dict = {
    "false": False,
    "true": True
}

def window_matches_keybind(keyb : Keybind) -> bool:
    if current_window is None:
        if len(keyb.selectors) == 0:
            return True 
        return False
    
    succ = 0

    for selector in keyb.selectors:
        sel, val = selector.split(":")

        if sel == "class": sel = "window_class"
        if val in bool_dict: val = bool_dict[val]
        if type(val) == str and val.startswith("("): val = val[1:-1]
        win_val = getattr(current_window, sel)
        
        try:
            if type(val) == bool: raise re.error("re.error: window selector is a boolean")
            reg = re.compile(val)
            res = reg.match(win_val)
            if res is None: raise re.error("re.error: res is none")
            reg_res = res.group(0)
            succ += reg_res == win_val
        except re.error as e:
            logger.debug(f"socket > window matching > re.error: {e}")
            succ += (win_val == val)

        logger.debug(f"socket > window matching > sel: {sel}: {val} | {win_val} ({win_val == val})")

    selector_n = len(keyb.selectors)
    return succ == selector_n if selector_n != 0 else False

def handle_keybind_activation() -> None:
    remove_keybinds()
    
    for keyb in app_keybinds:
        if window_matches_keybind(keyb):
            if not keyb.active:
                add_keybind(keyb)
        else:
            if keyb.bind_type == "unbind":
                remove_keybind(keyb)

def reload_keybinds() -> None:
    global app_keybinds
    fileloc = conf_parser.get_conf_file_loc()
    hyprvars = get_vars_from_file(fileloc)
    config = conf_parser.read_keybinds_file(conf_parser.get_conf_file_loc())

    remove_keybinds()
    app_keybinds = conf_parser.parse_key_lines(config, hyprvars)
    handle_keybind_activation()
     
    logger.debug("reloaded conf.")

def remove_keybinds() -> None:
    for keyb in app_keybinds:
        remove_keybind(keyb) if keyb.bind_type == "bind" else add_keybind(keyb)

def add_unbind_keybinds() -> None:
    for i in app_keybinds:
        if i.bind_type == "unbind":
            remove_keybind(i)

def at_exit() -> None:
    global running
    running = False
    if sock is not None: sock.close()

    logger.debug("exitting.")
    remove_keybinds()
    add_unbind_keybinds()
    sys.exit()


def handle_hup_signal(_sig, _frame): reload_keybinds()
def handle_sigterm_signal(_sig, _frame): at_exit()

def get_socket_path() -> str:
    hypr_inst_signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", None)

    if (hypr_inst_signature is None):
        logger.error("HIS not found")
        sys.exit(1)

    xdg_runtime_dir = os.environ.get("XDG_RUNTIME_DIR", None)
    if (xdg_runtime_dir is None):
        logger.error("XDG_RUNTIME_DIR not set.")
        sys.exit(2)

    socket_path = os.path.join(xdg_runtime_dir, "hypr", hypr_inst_signature, ".socket2.sock")

    if not os.path.exists(socket_path):
        logger.error("Socket doesnt exist (what?)")
        sys.exit(3)

    return socket_path


def create_socket(keybinds : List[Keybind]) -> NoReturn:
    global app_keybinds, sock
    app_keybinds = keybinds
    
    socket_path = get_socket_path()
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        signal.signal(signal.SIGHUP, handle_hup_signal)
        signal.signal(signal.SIGTERM, handle_sigterm_signal)

        sock.connect(socket_path)
        logger.info("connected to hyprland socket2")

        while running:
            data = sock.recv(4096)
            if not data:
                logger.error("hyprland socket closed (this shouldnt happen)")
                break

            on_event(data)
    except Exception as e:
        logger.error("socket error:", e)
    finally:
        sock.close()
        sys.exit()

def add_keybind(keybind_event) -> None:
    cmd = keybind_event.to_command()
    subprocess.run(cmd, capture_output=True)
    logger.debug(f"{'added' if keybind_event.bind_type == 'bind' else 'removed'} keybind: {cmd[-1]}")
    keybind_event.active = True # if keybind_event.bind_type == "bind" else False

def remove_keybind(keybind_event):
    cmd = keybind_event.to_command(True)
    subprocess.run(cmd, capture_output=True)
    logger.debug(f"{'removed' if keybind_event.bind_type == 'bind' else 'added'} keybind: {cmd[-1]}")
    keybind_event.active = False # if keybind_event.bind_type == "bind" else True

def on_event(event_text : bytes):
    if not running:
        return

    global current_window_class, current_window
    event : str = event_text.decode().strip()
    events = event.split("\n")

    for ev in events:
        event_type, event_data = ev.split(">>")
        if (event_type != EVENT_WINDOW_FOCUSED):
            continue

        current_window = Window.from_address(f"0x{event_data}")
        if current_window is not None:
            logger.debug(f"Window focused: {current_window.title} (class: {current_window.window_class})")
        else:
            logger.debug("Lost window focus")

        handle_keybind_activation() 

