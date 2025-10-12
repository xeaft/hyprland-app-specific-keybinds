from typing import Optional, List, Dict, Any
from dataclasses import dataclass, fields
import subprocess
import json

@dataclass
class Window:
    address: str = "" 
    mapped: Optional[bool] = None
    hidden: Optional[bool] = None
    workspace: Optional[int] = None
    floating: Optional[bool] = None
    pseudo: Optional[bool] = None
    monitor: Optional[int] = None
    window_class: Optional[str] = None
    title: Optional[str] = None
    initialClass: Optional[str] = None
    initialTitle: Optional[str] = None
    pid: Optional[int] = None
    xwayland: Optional[bool] = None
    pinned: Optional[bool] = None
    fullscreen: Optional[int] = None
    grouped: Optional[List[Any]] = None
    tags: Optional[List[Any]] = None
    swallowing: Optional[str] = None
    inhibitingIdle: Optional[bool] = None
    xdgTag: Optional[str] = None
    xdgDescription: Optional[str] = None

    @classmethod
    def from_address(cls, addr : str) -> "Window | None":
        res : List[Dict] = json.loads(subprocess.run(["hyprctl", "-j", "clients"], capture_output=True).stdout.decode())
        valid_keys = {f.name for f in fields(cls)}
        for dict_win in res:
            if not dict_win["address"] == addr:
                continue
            
            filtered_data = {k: v for k, v in dict_win.items() if k in valid_keys}
            win = Window(**filtered_data)
            win.window_class = dict_win["class"]
            return win
        
        return None

