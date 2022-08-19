import logging
from enum import Enum

class OperationType(Enum):
    INIT = 'init'
    START = 'start'
    SETUP = 'setup'
    STOP = 'stop'
    RESTART = 'restart'
    CLEAN = 'clean'
    DESTROY = 'destroy'
    RESET = 'reset'
    STATUS = 'status'
    Scaffold = 'scaffold'

    def __str__(self):
        return self.value

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class OutputStream(Enum):
    STDOUT = 'stdout'
    STDERR = 'stderr'
    STDNULL = 'stdnull'

class LogLevel(Enum):
    DEBUG=str(logging.DEBUG)
    INFO=str(logging.INFO)
    WARNING=str(logging.WARNING)
    ERROR=str(logging.ERROR)
    CRITICAL=str(logging.CRITICAL)

    def __str__(self):
        return str(self.value)