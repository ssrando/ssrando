import os
from pathlib import Path

try:
    # can be imported if running the binary
    from sys import _MEIPASS

    RANDO_ROOT_PATH = Path(_MEIPASS)
    IS_RUNNING_FROM_SOURCE = False
except ImportError:
    RANDO_ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__)))
    IS_RUNNING_FROM_SOURCE = True
