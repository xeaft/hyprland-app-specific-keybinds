from typing import Any

class HyprVar:
    def __init__(self, name : str, val : Any):
        self.name : str = name
        self.val : str = str(val)
