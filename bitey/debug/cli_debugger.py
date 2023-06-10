from dataclasses import dataclass
import logging
import readline  # noqa: F401

from bitey.debug.debugger import Debugger

module_logger = logging.getLogger("bitey.debug")


@dataclass
class CLIDebugger(Debugger):
    def __post_init__(self):
        "Create the debugger"
        self.logger = logging.getLogger("bitey.debug.cli_debugger.CLIDebugger")
        self.computer.set_input_handler(self.input_handler)

    def input_handler(self):
        """
        Use this Debugger TUI as an input handler for normal code
        """
        return input("> ")
