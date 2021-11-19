from dataclasses import dataclass
import json
from json import JSONDecoder
from typing import ClassVar


from bitey.cpu.addressing_mode import (
    # AbsoluteAddressingMode,
    # ImmediateAddressingMode,
    ImpliedAddressingMode,
)
from bitey.cpu.instruction.instruction import Instruction, Instructions
from bitey.cpu.instruction.instruction_json_decoder import (
    InstructionsJSONDecoder,
)

from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.sei import SEI

# from bitey.cpu.instruction.ldx import LDX
# from bitey.cpu.instruction.txs import TXS
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.cpu.flag.flag import Flags, FlagsJSONDecoder
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


@dataclass
class CPU:
    """
    CPU Class
    TODO: Refactor using a builder pattern
    """

    stack_start: ClassVar[int] = 0x01FF
    """
    Start of the stack
    This location is "Page One"
    """

    stack_size: ClassVar[int] = 0x0100
    """
    Maximum stack size
    The stack is automatically locatd in "Page One".  Page size is 0x0100
    """

    registers: Registers

    flags: Flags

    instructions: Instructions

    pins: Pins

    current_instruction: Instruction = None

    def __post_init__(self):
        """
        Called after the generated __init__ method
        Initialize the processor.
        """
        return

    def reset(self, memory):
        "Reset the CPU"

        # Disable interrupts
        # TODO: The flags need to be initialized to some valid
        # boolean state before running this
        self.flags.data = 0

        # TODO: Use a different builder for this
        opcodes = Opcodes([Opcode(120, ImpliedAddressingMode)])
        sei = SEI("SEI", opcodes, "Set Interrupt Disable")
        sei.execute(self, memory)

        # Set the PC to the value at 0xFFFC and 0xFFFD
        self.registers["PC"].value = memory.get_16bit_value(0xFFFC, 0xFFFD)

        # TODO: Verify, this may not be in the reference
        # Processor Status Register still needs to be initialized
        self.registers["A"].value = 0xFF
        self.registers["X"].value = 0xFF
        self.registers["Y"].value = 0xFF
        self.registers["P"].value = 0xFF

        # Load the first instruction
        self.load_instruction(memory)

        # Initialize the stack
        self.stack_init()

        # TODO: Initialize data devices

        # TODO: CLI to enable interrupts
        opcodes = Opcodes([Opcode(88, ImpliedAddressingMode)])
        cli = CLI("CLI", opcodes, "Clear Interrupt Disable")
        cli.execute(self, memory)

        # TODO: Initialize the decimal mode
        # For now, test with all flags initialized to zero
        # This is dependent on the application,
        self.flags.data = 0

        #   TODO: Start the user's program

    def build_from_json(json_data):
        decoder = CPUJSONDecoder()
        cpu = decoder.decode(json_data)

        return cpu

    def load_instruction(self, memory):
        self.current_instruction = self.get_next_instruction(memory)
        # TODO: May need to refactor this for immediate addressing mode or other
        # models
        self.registers["PC"].value += 1

    def get_next_instruction(self, memory):
        return self.registers["PC"].value

    def execute_instruction(self, memory):
        "Execute an instruction"
        self.current_instruction.execute(self, memory)

    def set_flags(self, instruction, flags, registers):
        "Set flags depending on the instruction"
        instruction.set_flags(flags, registers)

    def stack_init(self):
        """
        Initialize the stack
        The stack starts at 0x01FF and moves downwards
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
        # CPU reference documentation is ambiguous in defining what actual value
        # the stack pointer should store, and how the final address should be
        # calculated.
        # These stack routines assume the address is stored directly in the
        # stack pointer, and not calculated by adding 0x0100
        # to the contents of the stack pointer to get the memory address
        # for a page zero stack, for a page one stack it would be 0x01FF
        # (This means the stack pointer would start at zero)
        #
        # TODO: This can also be done by LDX and TXS instructions
        # But since an immediate LDX instruction can store a max value of 0xFF,
        # some sort of extra addition would be needed, or an absolute
        # mode version
        # ldx = LDX(
        #     "LDX",
        #     Opcodes([Opcode(174, AbsoluteAddressingMode())]),
        #     "Load Index Register X From Memory",
        # )
        # txs = TXS(
        #     "TXS",
        #     Opcodes([Opcode(154, ImpliedAddressingMode())]),
        #     "Transfer index X to stack pointer",
        # )

        self.registers["S"].value = 0x01FF

    def stack_push(self, memory, value):
        "Push a value on the stack"
        stack_pointer = self.registers["S"].value
        if (CPU.stack_start - stack_pointer) >= CPU.stack_size:
            raise StackOverflow

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
        # TODO: These stack routines may be wrong, we may need to add 0x0100
        # to the contents of the stack pointer to get the memory address
        stack_pointer = self.registers["S"].value
        if CPU.stack_start == stack_pointer:
            raise StackUnderflow

        self.registers["S"].value = self.registers["S"].value + 1
        stack_pointer = self.registers["S"].value

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


class CPUJSONDecoder(JSONDecoder):
    """
    Decode a CPU in JSON format
    """

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

        instructions = None
        if "instructions" in parsed_json:
            instructions_decoder = InstructionsJSONDecoder()
            instructions = instructions_decoder.decode_parsed(
                parsed_json["instructions"]
            )

        cpu = CPU(registers, flags, instructions, Pins([]))
        return cpu
