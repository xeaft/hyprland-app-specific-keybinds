import logging
import os

levels = [logging.INFO, logging.DEBUG]
level = levels[1] if os.environ.get("DEBUG_LOG") is not None else levels[0]

RESET = "\033[0m"
COLORS = {
    "DEBUG": "\033[36m",
    "INFO": RESET,
    "WARNING": "\033[33m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[31m",
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = COLORS.get(record.levelname, RESET)
        record.levelname = f"{color}{record.levelname}{RESET}"
        return super().format(record)

handler = logging.StreamHandler()
formatter = ColorFormatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(level)
logger.addHandler(handler)
