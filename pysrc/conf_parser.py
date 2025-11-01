import os
import re
import sys
from keybind import Keybind
from typing import List, Literal, cast
from hyprvarparser import _parse_hyprlang_right_comp, get_vars_from_file
from hyprvar import HyprVar
from glog import logger

def get_conf_file_loc() -> str:
    config_path = os.environ.get("XDG_CONFIG_HOME", None)

    if config_path is None:
        logger.error("XDG_CONFIG_HOME is not present.")
        sys.exit(1) 

    custom_hypr = os.environ.get("HYRPCONF", None)

    hypr_conf_path = os.path.join(config_path, "hypr" if custom_hypr is None else custom_hypr)

    if not os.path.exists(hypr_conf_path):
        logger.error(f"Hyprland config directory doesnt exist. ({hypr_conf_path})")
        sys.exit(2)

    custom_key_file = os.environ.get("KEYCONF", None)
    key_conf_file = os.path.join(hypr_conf_path, "windowkeys.conf" if custom_key_file is None else custom_key_file)

    if not os.path.isfile(key_conf_file):
        logger.error(f"Keybinds file not found. ({key_conf_file})")
        return ""

    return key_conf_file

def read_keybinds_file(conf_file : str) -> List[str]:
    if not len(conf_file):
        return []

    with open(conf_file, "r") as f:
        return f.readlines()

def parse_bind_line(line : str) -> Keybind|None:
    reg = re.compile(r'^(bind|unbind)([a-z]*)\s*=\s*((?:[^,]+(?:\:[^,]+)?(?:\s+[^,]+:[^,]+)*)?)(?:,\s*([^,]*))?(?:,\s*([^,]*))?(?:,\s*([^,]*))?(?:,\s*(.*))?')
    res = reg.match(line)
    
    if not (res and len(res.groups()) == 7):
        return None 
    
    bind_type, bind_args, selectors_raw, mods, key, disp, args = res.groups()
    if selectors_raw == None: selectors_raw = ""

    if bind_type not in ["unbind", "bind"]:
        logger.warning(f"Invalid keyword (bind/unbind expected, '{bind_type}' recieved)")
        return None 

    bind_type = cast(Literal["unbind", "bind"], bind_type)
    selectors = re.findall(r'\w+:\([^)]+\)|\w+:\S+', selectors_raw)
    return Keybind(bind_type, selectors, mods, key, disp, args, bind_args, False if bind_type == "bind" else True)


def parse_key_lines(lines : List[str], hyprvars : List[HyprVar] = []) -> List[Keybind]:
    keybinds : List[Keybind] = []
    
    for line in lines:
        comment_index = line.find("#")
        if comment_index != -1:
            line = line[:comment_index]
        
        split = line.split("=")
        if len(split) < 2:
            continue

        left, right = split[0].strip(), "=".join(split[1:]).strip()
        if right.find("$") != -1:
            right = _parse_hyprlang_right_comp(right, hyprvars)

        if left.startswith("bind") or left.startswith("unbind"):
            keybind = parse_bind_line(line)
            if keybind is not None:
                keybinds.append(keybind)

        if left in ["var", "varfile", "source"]:
            hyprvars = hyprvars + get_vars_from_file(os.path.expanduser(os.path.expandvars(right)))

    return keybinds
        
