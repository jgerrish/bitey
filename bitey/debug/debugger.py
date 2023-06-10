from dataclasses import dataclass
from enum import Enum
import logging

from bitey.logger import setup_logger
from bitey.computer.computer import Computer

from bitey.cpu.cpu import CPUBreakpoint, CPUState, CPUStateChange

module_logger = logging.getLogger("bitey.debug")


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


@dataclass
class Debugger:
    """
    Abstract base class for debugger implementations
    """

    computer: Computer
    "The Computer this debugger manages"

    state: DebuggerState = DebuggerState.STOPPED
    "The current state of the debugger"

    def __post_init__(self):
        setup_logger()
        self.logger = logging.getLogger("bitey.debug.debugger.Debugger")

    def run(
        self, num_instructions_loaded_limit=None, num_instructions_executed_limit=None
    ):
        """
        Run the debugger
        """
        self.computer.set_instructions_loaded_limit(num_instructions_loaded_limit)
        self.computer.set_instructions_executed_limit(num_instructions_executed_limit)
        self.event_loop()

    def set_state(self, state):
        """
        Change the debugger state.

        If the new state is different from the previous state, raise a
        DebuggerStateChange exception.
        """
        if self.state != state:
            self.state = state
            raise DebuggerStateChange(state)

    def event_loop(self):  # noqa: C901
        """
        The event loop for the debugger.

        This continues running until a processor or memory state
        change is detected.  Then the debugger asks the user for a
        command or prints out information.
        """
        first_run = True
        while True:
            try:
                if self.state == DebuggerState.RUNNING:
                    print("Running\n")
                    self.computer.run(first_run)
                elif (
                    (self.state == DebuggerState.STEPPING)
                    or (self.state == DebuggerState.STOPPED)
                    or (self.state == DebuggerState.BREAKPOINT)
                ):
                    command = self.input_handler()
                    print("\nCommand: {}\n".format(command))
                    if command == "s":
                        # When stepping through code, breakpoints are
                        # printed but "ignored", execution is not
                        # stopped.
                        instruction_loaded = first_run
                        if self.state == DebuggerState.BREAKPOINT:
                            self.computer.cpu.ignore_breakpoints_until_next_instruction = (
                                True
                            )
                            instruction_loaded = True
                        self.state = DebuggerState.STEPPING
                        self.computer.step(instruction_loaded)
                    elif command == "c":
                        instruction_loaded = first_run
                        if self.state == DebuggerState.BREAKPOINT:
                            self.computer.cpu.ignore_breakpoints_until_next_instruction = (
                                True
                            )
                            instruction_loaded = True
                        self.state = DebuggerState.RUNNING
                        self.logger.debug("Running")
                        self.computer.run(instruction_loaded)
                        first_run = False
                        self.state = DebuggerState.STOPPED
                    elif command == "m":
                        memory_dump = self.computer.memory.memory_dump()
                        print("zeropage memory:\n{}".format(memory_dump))
                    elif command == "r":
                        print(self.computer.cpu.registers)
                    elif command == "f":
                        print(self.computer.cpu.flags)
                    elif command == "q":
                        self.set_state(DebuggerState.EXIT)
                    elif (command == "h") or (command == "?"):
                        print(
                            "[c]: continue, [s]: step, [m]: dump zero page memory, [f]: dump flags, [r]: dump registers, [q]: quit, [h,?]: help\n"  # noqa: E501
                        )

            except CPUStateChange as e:
                self.logger.debug("CPUState changed: {}".format(e.state))
                if e.state == CPUState.STOPPED:
                    self.state = DebuggerState.STOPPED
                    self.logger.debug("set debugger state to stopped")
                elif e.state == CPUState.RUNNING:
                    self.state = DebuggerState.RUNNING
                    self.logger.debug("set debugger state to running")
            except CPUBreakpoint as bp:
                self.logger.debug("Breakpoint reached: 0x{:04x}".format(bp.args[0]))
                # When stepping through code, breakpoints are printed
                # but "ignored" and execution is not stopped.
                if self.state != DebuggerState.STEPPING:
                    self.state = DebuggerState.BREAKPOINT
            except DebuggerStateChange as dsc:
                raise dsc
            except Exception as e:
                self.logger.debug("Exception caught: {}".format(e))
                print("Exception caught: {}".format(e))
                self.set_state(DebuggerState.EXIT)
