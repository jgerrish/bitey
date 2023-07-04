from dataclasses import dataclass, field
from typing import List


@dataclass
class Config:
    """
    Configuration class for the debugger
    """

    breakpoints: List = field(default_factory=lambda: [])
    "The breakpoint configuration data"

    watchpoints: List = field(default_factory=lambda: [])
    "The watchpoint configuration data"

    def __str__(self):
        res = ""
        if len(self.breakpoints) > 0:
            res += "  Breakpoints:\n"
            for bp in self.breakpoints:
                res += "    description: {}\n".format(bp["description"])
                res += "    address: 0x{:04X}\n".format(bp["address"])

        if len(self.watchpoints) > 0:
            res += "  Watchpoints:\n"
            for wp in self.breakpoints:
                res += "    description: {}\n".format(wp["description"])
                res += "    address: 0x{:04X}\n".format(wp["address"])

        return res

    def apply(self, debugger):
        """
        Apply the configuration to a debugger
        """
        for bp in self.breakpoints:
            if "address" in bp:
                debugger.computer.cpu.set_breakpoint(bp["address"])
        for wp in self.watchpoints:
            if "address" in wp:
                debugger.computer.cpu.set_watchpoint(
                    wp["address"], debugger.computer.memory
                )
