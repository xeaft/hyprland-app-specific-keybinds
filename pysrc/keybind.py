from typing import List, Literal

class Keybind:
    def __init__(self, bind_type: Literal["bind", "unbind"], selectors : List[str], mod : str, key : str, dispatcher : str, params : str, bind_flags : str = "", active : bool = False):
        self.bind_type = bind_type
        self.selectors = selectors
        self.mod = mod
        self.key = key
        self.dispatcher = dispatcher
        self.params = params
        self.flags = bind_flags if bind_flags is not None else ""
        self.active = active

    def to_command(self, reverse : bool = False) -> List[str]:
        if (self.bind_type == "bind") != reverse: return ["hyprctl", "keyword", "--", f"bind{self.flags}", f"{self.mod},{self.key},{self.dispatcher},{self.params}"]
        return ["hyprctl", "keyword", "unbind", f"{self.mod},{self.key}"]
