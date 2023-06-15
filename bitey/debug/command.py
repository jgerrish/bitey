from dataclasses import dataclass
from typing import ClassVar

from bitey.debug.debugger_state import DebuggerState


@dataclass
class Command:
    """
    Debugger command parser
    """

    commands: ClassVar[dict] = {
        "step": "step",
        "continue": "continue",
        "memory": "memory",
        "x": "memory",
        "flags": "flags",
        "registers": "registers",
        "quit": "quit",
        "help": "help",
        "?": "help",
    }

    command_string: str
    "The command string to parse"

    def __post_init__(self):
        self.parse()

    def parse(self):
        """Parse the command string"""

        # split on spaces
        self.parsed = self.command_string.split(" ")

        # For now, we'll just do a prefix substring match on each individual command
        # It's not as efficient as a Trie, but it gets the job done
        # Return the first successful match
        self.command = None
        for c in self.commands:
            if c.find(self.parsed[0]) == 0:
                self.command = self.commands[c]

    def execute(self, debugger):  # noqa: C901
        """
        Execute a command with a given debugger
        """
        if self.command == "step":
            # When stepping through code, breakpoints are
            # printed but "ignored", execution is not
            # stopped.
            instruction_loaded = debugger.first_run
            if debugger.state == DebuggerState.BREAKPOINT:
                debugger.output_handler("Breakpoint")
                debugger.computer.cpu.ignore_breakpoints_until_next_instruction = True
                instruction_loaded = True
            debugger.state = DebuggerState.STEPPING
            debugger.computer.step(instruction_loaded)
            debugger.print_next_instruction()
            debugger.first_run = False
        elif self.command == "continue":
            instruction_loaded = debugger.first_run
            if debugger.state == DebuggerState.BREAKPOINT:
                debugger.computer.cpu.ignore_breakpoints_until_next_instruction = True
                instruction_loaded = True
            debugger.state = DebuggerState.RUNNING
            debugger.logger.debug("Running")
            debugger.computer.run(instruction_loaded)
            debugger.first_run = False
            debugger.state = DebuggerState.STOPPED
        elif self.command == "memory":
            if len(self.parsed) == 1:
                memory_dump = debugger.computer.memory.memory_dump()
                debugger.output_handler("zeropage memory:\n{}".format(memory_dump))
            elif len(self.parsed) == 2:
                start = int(self.parsed[1], base=0)
                memory_dump = debugger.computer.memory.memory_dump(start)
                debugger.output_handler("memory:\n{}".format(memory_dump))
            else:
                memory_dump = debugger.computer.memory.memory_dump()
                debugger.output_handler("memory:\n{}".format(memory_dump))
        elif self.command == "registers":
            debugger.output_handler(debugger.computer.cpu.registers)
        elif self.command == "flags":
            debugger.output_handler(debugger.computer.cpu.flags)
        elif self.command == "quit":
            debugger.set_state(DebuggerState.EXIT)
        elif self.command == "help":
            debugger.output_handler(
                "[c]: continue, [s]: step, [m,x] [start]: dump memory, [f]: dump flags, [r]: dump registers, [q]: quit, [h,?]: help\n"  # noqa: E501
            )
