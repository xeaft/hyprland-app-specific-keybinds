from typing import List

class Keybind:
    def __init__(self, selectors : List[str], mod : str, key : str, dispatcher : str, params : str, bind_flags : str = ""):
        self.selectors = selectors
        self.mod = mod
        self.key = key
        self.dispatcher = dispatcher
        self.params = params
        self.flags = bind_flags if bind_flags is not None else ""
        self.active = False

    def to_command(self, unbind : bool = False) -> List[str]:
        if not unbind:
            return ["hyprctl", "keyword", "--", f"bind{self.flags}", f"{self.mod},{self.key},{self.dispatcher},{self.params}"]

        return ["hyprctl", "keyword", "unbind", f"{self.mod},{self.key}"]
