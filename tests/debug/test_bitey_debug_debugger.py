from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU
from bitey.debug.debugger import Debugger, DebuggerState, DebuggerStateChange
from collections import deque
from dataclasses import dataclass, field
import logging
from typing import Deque


def build_cpu():
    f = open("chip/6502.json")
    chip_data = f.read()

    cpu = CPU.build_from_json(chip_data)

    return cpu


# Create a mock debugger that can be driven by a queue of commands
@dataclass
class MockDebugger(Debugger):
    "A mock debugger that can be driven by an array of commands"

    commands: Deque = field(default_factory=lambda: deque())
    "The list of commands for the debugger"

    def __post_init__(self):
        "Create the debugger"
        self.logger = logging.getLogger("bitey.debug.mock_debugger.MockDebugger")
        self.computer.set_input_handler(self.input_handler)

    def input_handler(self):
        """
        Use this Debugger TUI as an input handler for normal code
        """
        return self.commands.popleft()

    def output_handler(self, string):
        """
        The output handler for the mock debugger prints to stdout
        """
        print(string)


def test_bitey_debug_debugger_run():
    """
    This is a simple test of the debugger.

    It sets up a breakpoint and command queue and tests that the first
    command is executed.
    """
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()

        computer = Computer.build_from_json(chip_data)

        assert len(computer.memory.memory) == 65536

    # Three NOP instructions
    computer.memory.write(0x01, 0xEA)
    computer.memory.write(0x02, 0xEA)
    computer.memory.write(0x03, 0xEA)

    # Break on the first instruction
    computer.cpu.set_breakpoint(0x00)

    # Create a queue of debugger commands to feed to the debugger when
    # it needs input.
    debugger_commands = deque(["q"])

    debugger = MockDebugger(computer, DebuggerState.STOPPED, debugger_commands)

    assert debugger.state == DebuggerState.STOPPED
    instructions_loaded_limit = 3
    instructions_executed_limit = 3
    try:
        debugger.run(instructions_loaded_limit, instructions_executed_limit)
    except DebuggerStateChange as e:
        # After the breakpoint is triggered, the debugger will read
        # the next command from the command queue.  This command is
        # "q" (quit).  The debugger will throw a DebuggerStateChange
        # exception and we catch it here.
        assert e.state == DebuggerState.EXIT
    else:
        assert False
