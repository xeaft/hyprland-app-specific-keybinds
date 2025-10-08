class Keybind:
    def __init__(self, window_class : str, mod : str, key : str, dispatcher : str, params : str, bind_flags : str = ""):
        self.winclass = window_class
        self.mod = mod
        self.key = key
        self.dispatcher = dispatcher
        self.params = params
        self.flags = bind_flags if bind_flags is not None else ""
        self.active = False

    def to_command(self, unbind : bool = False) -> str:
        if not unbind:
           return f"hyprctl keyword -- bind{self.flags} {self.mod},{self.key},{self.dispatcher},{self.params}"
        return f"hyprctl keyword unbind {self.mod},{self.key}"
