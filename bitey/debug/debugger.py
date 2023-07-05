from dataclasses import dataclass
import logging

from bitey.debug.command import Command
from bitey.debug.debugger_state import DebuggerState, DebuggerStateChange
from bitey.logger import setup_logger
from bitey.computer.computer import Computer

from bitey.cpu.cpu import CPUBreakpoint, CPUState, CPUStateChange

module_logger = logging.getLogger("bitey.debug")


@dataclass
class Debugger:
    """
    Abstract base class for debugger implementations
    """

    computer: Computer
    "The Computer this debugger manages"

    state: DebuggerState = DebuggerState.STOPPED
    "The current state of the debugger"

    eval_enabled: bool = False
    "A flag indicating whether Python evaluation is enabled in the debugger"

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
        self.first_run = False
        while True:
            try:
                if self.state == DebuggerState.RUNNING:
                    self.output_handler("Running\n")
                    self.computer.run(self.first_run)
                elif (
                    (self.state == DebuggerState.STEPPING)
                    or (self.state == DebuggerState.STOPPED)
                    or (self.state == DebuggerState.BREAKPOINT)
                ):
                    command = self.input_handler()
                    parsed_command = Command(command, eval_enabled=self.eval_enabled)
                    parsed_command.execute(self)
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
                self.state = DebuggerState.BREAKPOINT
                self.output_handler("Breakpoint")
                self.print_next_instruction()
            except DebuggerStateChange as dsc:
                raise dsc
            except Exception as e:
                self.logger.debug("Exception caught: {}".format(e))
                self.output_handler("Exception caught: {}".format(e))
                self.set_state(DebuggerState.EXIT)

    def print_next_instruction(self):
        """
        Print the next instruction
        The assembly_str method changes the PC.
        This was an initial design decision that should probably be changed.
        """
        pc = self.computer.cpu.registers["PC"].value
        instruction = self.computer.cpu.peek_next_instruction(self.computer.memory)
        # This is really hacky, think about better ways
        self.computer.cpu.registers["PC"].set(pc + 1)
        asm_str = instruction.assembly_str(self.computer)
        self.output_handler("0x{:04X} {}".format(pc, asm_str))
        self.computer.cpu.registers["PC"].set(pc)
