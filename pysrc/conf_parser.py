import os
import re
import sys
from keybind import Keybind
from typing import List

def get_conf_file_loc() -> str:
    config_path = os.environ.get("XDG_CONFIG_DIRS", None)

    if config_path is None:
        print("XDG_CONFIG_DIRS is not present.")
        sys.exit(1) 

    custom_hypr = os.environ.get("HYRPCONF", None)

    hypr_conf_path = os.path.join(config_path, "hypr" if custom_hypr is None else custom_hypr)

    if not os.path.exists(hypr_conf_path):
        print(f"Hyprland config directory doesnt exist. ({hypr_conf_path})")
        sys.exit(2)

    custom_key_file = os.environ.get("KEYCONF", None)
    key_conf_file = os.path.join(hypr_conf_path, "windowkeys.conf" if custom_key_file is None else custom_key_file)

    if not os.path.isfile(key_conf_file):
        print(f"Keybinds file not found. ({key_conf_file})")
        return ""

    return key_conf_file

def read_keybinds_file() -> List[str]:
    conf_file = get_conf_file_loc()
    if not len(conf_file):
        return []

    with open(conf_file, "r") as f:
        return f.readlines()

def parse_key_lines(lines : List[str]) -> List[Keybind]:
    keybinds : List[Keybind] = []
    
    for line in lines:
        comment_index = line.find("#")
        if comment_index != -1:
            line = line[:comment_index]
        
       
        reg = re.compile(r'^\s*bind(?:(\w+))?\s*=\s*((?:\w+:\([^)]+\)|\w+:\S+)(?:\s+(?:\w+:\([^)]+\)|\w+:\S+))*)?\s*,\s*(.*?)\s*,\s*(.*?)\s*,\s*(.*?)\s*,\s*(.*)$')

        res = reg.match(line)
        
        if not (res and len(res.groups()) == 6):
            continue
        
        bind_args, selectors_raw, mods, key, disp, args = res.groups()
        if selectors_raw == None: selectors_raw = ""
        selectors = re.findall(r'\w+:\([^)]+\)|\w+:\S+', selectors_raw)
        keybind = Keybind(selectors, mods, key, disp, args, bind_args)
        keybinds.append(keybind)

    return keybinds
        
