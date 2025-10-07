class Keybind:
    def __init__(self, mod : str, key : str, dispatcher : str, params : str, bind_flags : str = ""):
        self.mod = mod
        self.key = key
        self.dispatcher = dispatcher
        self.params = params
        self.flags = bind_flags

    def to_command(self, unbind : bool = False) -> str:
        return f"hyprctl keyword -- {'' if not unbind else 'un'}bind{self.flags} {self.mod},{self.key}{self.dispatcher}{self.params}"
