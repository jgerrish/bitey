from dataclasses import dataclass, field
from enum import Enum
import json
import logging
from json import JSONDecoder
from typing import ClassVar, Dict


from bitey.cpu.addressing_mode import (
    # AbsoluteAddressingMode,
    # ImmediateAddressingMode,
    ImpliedAddressingMode,
)
from bitey.cpu.instruction.instruction import Instruction, InstructionSet
from bitey.cpu.instruction.instruction_json_decoder import InstructionSetJSONDecoder

from bitey.cpu.instruction.cld import CLD
from bitey.cpu.instruction.cli import CLI

# from bitey.cpu.instruction.sei import SEI

# from bitey.cpu.instruction.ldx import LDX
# from bitey.cpu.instruction.txs import TXS
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.cpu.flag.flag import Flags
from bitey.cpu.flag.flag_json_decoder import FlagsJSONDecoder
from bitey.cpu.pin import Pins
from bitey.cpu.register import (
    Registers,
    RegistersJSONDecoder,
)


class StackOverflow(Exception):
    """
    Stack overflow exception
    Raised if a push would extend the stack beyond the size of the stack
    """


class StackUnderflow(Exception):
    """
    Stack underflow exception
    Raised if a pop would move the stack before the start of the stack
    """


class CPUBreakpoint(Exception):
    """
    CPU Breakpoint exception
    Raised if a cpu breakpoint is hit
    """

    def __init__(self, address):
        self.address = address


class CPUStateChange(Exception):
    """
    CPUStateChange exception
    Raised if a change in cpu state occurs
    """

    def __init__(self, state):
        self.state = state


class CPUState(Enum):
    """
    Different CPU states.
    A CPU can be stopped or running.
    """

    STOPPED = 0
    RUNNING = 1


@dataclass
class CPU:
    """
    CPU Class
    TODO: Refactor using a builder pattern
    """

    stack_base: ClassVar[int] = 0x0100
    """
    Base offset of the stack
    This location is "Page One"
    """

    stack_size: ClassVar[int] = 0x0100
    """
    Maximum stack size
    The stack is automatically located in "Page One".  Page size is 0x0100
    """

    registers: Registers

    flags: Flags

    instruction_set: InstructionSet

    pins: Pins

    current_instruction: Instruction = None

    state: CPUState = CPUState.STOPPED
    """
    The current state of the CPU
    The CPU can be in several states, for example, STOPPED or RUNNING.

    CPU methods such as step() don't explicitly start the CPU running,
    but a caller may start the CPU before calling step() or run().
    """

    num_instructions_loaded: int = 0
    "The number of instructions that have been loaded by the processor"

    num_instructions_executed: int = 0
    "The number of instructions that have been executed by the processor"

    cpu_breakpoints: Dict = field(default_factory=lambda: {})
    "A dictionary of all CPU breakpoints"

    ignore_breakpoints_until_next_instruction: bool = False
    "Ignore breakpoints until the next instruction is loaded"

    def __post_init__(self):
        """
        Called after the generated __init__ method
        Initialize the processor.
        """
        self.logger = logging.getLogger("bitey.cpu.cpu")
        # TODO: Research best practices around logging and module namespaces
        self.registers.set_logger(self.logger)

        # Set the number of instructions that can be loaded to None,
        # so there is no limit
        self.num_instructions_loaded_limit = None
        # Set the number of instructions that can be executed to None,
        # so there is no limit
        self.num_instructions_executed_limit = None

        # Connect up the P register and flags with the Watcher/Listener API
        # We can profile later if speed is an issue
        if self.registers and self.flags:
            register = self.registers["P"]
            register.register(self.flags.pflag_listener)

            # Connect up the flags and the P register so they are both in sync
            self.flags.register(register.flags_listener)

        return

    def reset(self, memory, housekeeping=True, load_first_instruction=True):
        """
        Reset the CPU
        Reset the CPU, setting up the stack and other initial values.

        This loads the first instruction and increments the PC to the next instruction.

        This reset, restart and initialization process is outlined on
        page 125 of the MCS6500 Microcomputer Family Programming
        Manual.  The restart process includes executing several
        instructions such as CLI and CLD.  These steps are referred to
        as housekeeping in the manual.

        These instructions are counted towards the processor execution
        counts and limits.

        Some users of this module may not want to execute these
        instructions, if the instructions are already in their
        application.

        If housekeeping is True, the following occurs:
          A CLI and CLD instruction are executed.

        The first instruction in memory is loaded.
        """

        self.logger.debug("Resetting CPU")
        # Disable interrupts
        # TODO: The flags need to be initialized to some valid
        # boolean state before running this
        self.flags.data = 0

        self.num_instructions_loaded = 0
        self.num_instructions_loaded_limit = None
        self.num_instructions_executed = 0
        self.num_instructions_executed_limit = None

        # TODO: Use a different builder for this
        # opcodes = Opcodes([Opcode(120, ImpliedAddressingMode)])
        # sei = SEI("SEI", opcodes, "Set Interrupt Disable")
        # sei.execute(self, memory)

        # Set the PC to the value at 0xFFFC and 0xFFFD
        self.registers["PC"].value = memory.get_16bit_value(0xFFFC, 0xFFFD)

        # TODO: Verify, this may not be in the reference
        # Processor Status Register still needs to be initialized
        self.registers["A"].set(0x00)
        self.registers["X"].set(0x00)
        self.registers["Y"].set(0x00)
        self.registers["P"].set(0x00)

        # Load the first instruction and increment the PC
        if load_first_instruction:
            self.get_next_instruction(memory)

        # Initialize the stack
        self.stack_init()

        # TODO: Initialize data devices

        if housekeeping:
            opcodes = Opcodes([Opcode(88, ImpliedAddressingMode)])
            cli = CLI("CLI", opcodes, "Clear Interrupt Disable")
            cli.execute(self, memory)

            opcodes = Opcodes([Opcode(216, ImpliedAddressingMode)])
            cld = CLD("CLD", opcodes, "Clear Decimal Mode")
            cld.execute(self, memory)
            # The MOS 6502 family specification documents include a set of
            # instructions that should be run on reset.
            # These instructions are counted in the
            # num_instructions_loaded and num_instructions_executed
            # counters, even though they are not "technically" loaded from
            # memory, or loaded into normal CPU working area.
            # This may be confusing for those working with binary files
            # wondering where extra instructions are coming from.
            self.num_instructions_loaded += 2
            self.num_instructions_executed += 2

        # TODO: Initialize the decimal mode
        # For now, test with all flags initialized to zero
        # This is dependent on the application,
        self.flags.data = 0

        # The processor starts with the Break and Expansion flags set
        self.flags["B"].set()
        self.flags["E"].set()

        #   TODO: Start the user's program

    def set_state(self, state):
        """
        Change the processor state.

        If the new state is different from the previous state, raise a
        CPUStateChange exception.
        """
        if self.state != state:
            self.state = state
            raise CPUStateChange(state)

    def build_from_json(json_data):
        logger = logging.getLogger("bitey.cpu.cpu.CPU")
        decoder = CPUJSONDecoder()
        logger.debug("Building CPU")
        cpu = decoder.decode(json_data)

        return cpu

    def get_next_instruction(self, memory):
        """
        Load and decode the next instruction
        Increments the PC
        """
        if self.num_instructions_loaded_limit is not None:
            if self.num_instructions_loaded >= self.num_instructions_loaded_limit:
                self.set_state(CPUState.STOPPED)

        # Save the instruction address to test for breakpoints
        self.last_opcode_address = self.registers["PC"].value

        if not self.ignore_breakpoints_until_next_instruction and (
            self.last_opcode_address in self.cpu_breakpoints
        ):
            self.ignore_breakpoints_until_next_instruction = True
            raise CPUBreakpoint(self.last_opcode_address)
        else:
            self.ignore_breakpoints_until_next_instruction = False

        self.current_opcode = self.load_opcode(memory)
        self.logger.debug(
            "get_next_instruction opcode: {}, 0x{:2X}".format(
                self.current_opcode, self.current_opcode
            )
        )

        self.registers["PC"].inc()
        self.current_instruction = self.decode_opcode(self.current_opcode)

        return self.current_instruction

    def peek_next_instruction(self, memory):
        """
        Return the next instruction without incrementing the PC or
        changing the CPU state.
        """
        opcode = memory.read(self.registers["PC"].get())
        instruction = self.instruction_set.get_instruction_by_opcode(opcode)

        return instruction

    def load_opcode(self, memory):
        "Load the opcode pointed to by the PC from memory"
        self.logger.debug(
            "Loading opcode at 0x{:04X}".format(self.registers["PC"].get())
        )

        self.num_instructions_loaded += 1
        return memory.read(self.registers["PC"].get())

    def decode_opcode(self, opcode):
        "Decode the current opcode"
        # TODO: refactor this, figure out how to build cleaner
        # TODO: Add tests for this
        instruction = self.instruction_set.get_instruction_by_opcode(opcode)
        self.logger.debug("Decoded {}".format(instruction))

        return instruction

    def execute_instruction(self, memory):
        "Execute an instruction"
        if self.num_instructions_executed_limit is not None:
            if self.num_instructions_executed >= self.num_instructions_executed_limit:
                self.set_state(CPUState.STOPPED)

        self.logger.debug("Executing instruction")
        self.current_instruction.execute(self, memory)
        self.num_instructions_executed += 1

    def step(self, memory, count=1, instruction_loaded=False):
        """
        Execute the next count instructions, stepping into any subroutine calls
        Steps through one instruction if count isn't specified
        """
        for i in range(count):
            if not instruction_loaded:
                self.get_next_instruction(memory)
            self.execute_instruction(memory)

    def set_flags(self, instruction, flags, registers):
        "Set flags depending on the instruction"
        instruction.set_flags(flags, registers)

    def stack_init(self, stack_base=0x0100, stack_start=0xFF):
        """
        Initialize the stack.

        By default the stack starts at 0x01FF and moves downwards.

        The parameter stack_base is added to the stack address
        (usually the stack register).  It's set to 0x0100 by default.

        stack_start is set to the start (top) of the stack.  It is
        usually 0xFF.

        This would give an initial stack top of 0x01FF, the top-most
        value in Page One.

        The stack pointer always points to the next memory location data can be
        stored.
        The stack pointer size is 9.
        If you were storing something like the PC on the stack,
        the order of operations would be:
          push PC high
          push PC low
        So starting at 0x01FF, 0x1FF would be the high byte of the PC and
        0x1FE would be the low byte.

        """
        # Previous documentation about stack operation was incorrect.
        #
        # On page 116 of the MCS6500 Microcomputer Family Programming
        # Manual the operation of the stack is outlined.  By default,
        # it's automatically located in Page One.  "The microprocessor
        # always puts out the address 0x0100 plus stack register for
        # every stack operation."
        #
        # It also talks about "selected memory techniques" to locate
        # the stack in Page Zero or Page One.
        self.registers["S"].value = stack_start

    def stack_push(self, memory, value):
        "Push a value on the stack"
        stack_register = self.registers["S"].value
        if (CPU.stack_size - stack_register) > 0xFF:
            raise StackOverflow

        stack_pointer = CPU.stack_base + stack_register
        memory.write(stack_pointer, value)

        self.registers["S"].value = self.registers["S"].value - 1

    def stack_push_address(self, memory, address):
        """
        Push a 16-bit address on the stack
        Addresses are stored by storing the high byte first and then
        the low byte.
        For example, if the stack is empty, storing PC will store:
        0x01FF: the high byte of the PC
        0x01FE: the low byte of the PC
        """
        adh = (address & 0xFF00) >> 8
        adl = address & 0x00FF
        self.stack_push(memory, adh)
        self.stack_push(memory, adl)

    def stack_pop(self, memory):
        "Pop a  value off the stack"
        stack_register = self.registers["S"].value
        if (CPU.stack_size - stack_register) <= 0x01:
            raise StackUnderflow

        self.registers["S"].value = self.registers["S"].value + 1
        stack_register = self.registers["S"].value
        stack_pointer = CPU.stack_base + stack_register

        return memory.read(stack_pointer)

    def stack_pop_address(self, memory):
        """
        Pop a 16-bit address from the stack.

        Addresses are stored by storing the high byte first and then
        the low byte.
        For example, if the stack is empty, storing PC will store:
        0x01FF: the high byte of the PC
        0x01FE: the low byte of the PC
        """
        adl = self.stack_pop(memory)
        adh = self.stack_pop(memory)
        address = (adh << 8) | adl

        return address

    def stack_pull(self, memory):
        # TODO: These stack routines may be wrong, we may need to add 0x0100
        # to the contents of the stack pointer to get the memory address
        return self.stack_pop(memory)

    def stack_pull_address(self, memory):
        return self.stack_pop_address(memory)

    # Debugger related methods

    def set_breakpoint(self, address):
        "Set a breakpoint in the CPU"
        self.cpu_breakpoints[address] = True

    def clear_breakpoint(self, address):
        "Clear a breakpoint in the CPU"
        del self.cpu_breakpoints[address]


class CPUJSONDecoder(JSONDecoder):
    """
    Decode a CPU in JSON format
    """

    def __init__(self):
        self.logger = logging.getLogger("bitey.cpu.cpu.CPUJSONDecoder")

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        flags = None
        if "flags" in parsed_json:
            flags_decoder = FlagsJSONDecoder()
            flags = flags_decoder.decode_parsed(parsed_json["flags"])

        registers = None
        if "registers" in parsed_json:
            registers_decoder = RegistersJSONDecoder()
            registers = registers_decoder.decode_parsed(parsed_json["registers"])

        instruction_set = None
        if "instructions" in parsed_json:
            instruction_set_decoder = InstructionSetJSONDecoder()
            instruction_set = instruction_set_decoder.decode_parsed(
                parsed_json["instructions"]
            )

        cpu = CPU(registers, flags, instruction_set, Pins([]))
        return cpu
