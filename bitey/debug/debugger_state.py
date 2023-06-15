from enum import Enum


class DebuggerState(Enum):
    """
    Different debugging states.
    These are distinct from CPU states.
    A CPU can be stopped or running, but we want to also have states for the
    debugger to present different UI options.
    """

    STOPPED = 0
    RUNNING = 1
    STEPPING = 2
    EXIT = 3
    BREAKPOINT = 4


class DebuggerStateChange(Exception):
    """
    DebuggerStateChange exception
    Raised if a change in debugger state occurs
    """

    def __init__(self, state):
        self.state = state
