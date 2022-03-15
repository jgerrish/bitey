from dataclasses import dataclass
import logging

# from bitey.cpu.instruction.instruction_factory import InstructionFactory
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.memory.memory import MemoryOutOfRange


class UndocumentedInstruction(Exception):
    "This instruction is undocumented or invalid"


class UnimplementedInstruction(Exception):
    "The instruction is unimplemented"


class IncompleteInstruction(Exception):
    "The instruction is incomplete"


class UntestedInstruction(Exception):
    "The instruction is untested"


@dataclass
class Instruction:
    """
    A CPU instruction

    A CPU instruction is a class responsible for executing an
    instruction and updating any flags depending on the status.

    Instructions should not normally advance the PC.
    """

    # TODO: Extend to allow multiple opcodes and addressing modes
    # TODO: Building individual instrutions is a pain, there
    #       needs to be a better way to integrate the JSON description
    #       and the builder code

    name: str
    "The name of the instruction"

    opcode: Opcode = None
    "The instruction opcodes"

    description: str = None
    "A human-readable description of the instruction"

    def __post_init__(self):
        self.logger = logging.getLogger("bitey.cpu.instruction")

    def execute(self, cpu, memory):
        """
        Execute the instruction
        The execute method does not advance the instruction pointer to the next instruction
        unless the instruction itself modifies the PC.

        execute Gets the addressing mode and loads the value to operate on.

        Subclasses should implement instruction_execute for custom instruction code."
        """
        # TODO: There needs to be some refactoring around
        # Instruction and Opcode.
        # In particular, how should Instruction know which opcode
        # to execute
        # The current design idea:
        # Instructions loads instruction and opcode informaton from JSON
        # and provides an index to look up opcodes.
        # The InstructionFactory accepts an opcode and returns an
        # instruction wired up to execute that opcode
        self.logger.debug("Executing instruction: {}".format(self))

        # self.execute_opcode()
        # The instruction execution pattern is as follows:
        # First the base class execute method is called
        # Then the operand value is loaded from memory, based on the
        # addressing mode
        # Then the subclass instruction_execute is called if it exists
        if self.opcode is not None:
            self.logger.debug("addressing mode: {}".format(self.opcode.addressing_mode))
            (address, value) = self.opcode.addressing_mode.get_value(
                cpu.flags, cpu.registers, memory
            )

            self.logger.debug("address: {}, value: {}".format(address, value))

            self.instruction_execute(cpu, memory, value, address)
        else:
            raise UnimplementedInstruction

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Specific instruction subclasses should implement this
        method with their instruction code.
        Value is the value based on the addressing mode.
        """
        raise UnimplementedInstruction

    def get_opcode(self, opcode):
        return self.opcodes[opcode]

    def short_str(self):
        "The short name of the instruction, e.g. NOP"
        return "{}".format(self.name)

    def assembly_str(self, computer):
        """
        The string representing the disassembled instruction
        e.g. INC  0xCC
        It doesn't include the instruction address
        It requires a Computer argument, to print the instruction
        operand.
        """
        try:
            inst_str = self.opcode.addressing_mode.get_inst_str(
                computer.cpu.flags, computer.cpu.registers, computer.memory
            )
        except MemoryOutOfRange:
            inst_str = "INV"

        if inst_str != "":
            return "{}  {}".format(self.short_str(), inst_str)
        else:
            return "{}".format(self.short_str())


@dataclass
class InstructionClass:
    """
    A class of CPU instructions

    An Instruction is an individual instruction with a specific opcode

    An InstructionClass is a set of related opcodes gathered under a
    common instruction name.  The opcodes may specify different
    addressing modes or other things, but the instruction execution is
    essentially the same.

    An Instruction has an individual opcode associated with it.
    An InstructionClass has a set of opcodes associated with it.
    """

    name: str
    "The name of the instruction"

    instruction: Instruction
    "The actual Instruction class"

    opcodes: Opcodes
    "The instruction opcodes"

    description: str = None
    "A human-readable description of the instruction"

    def __post_init__(self):
        """
        Build the tables for opcode lookup
        """
        self.logger = logging.getLogger(
            "bitey.cpu.instruction.instruction.InstructionClass"
        )
        # Build the instruction database
        self.instructions = {}
        for opcode in self.opcodes:
            if self.instruction:
                # If self.instruction is set, then this is a subclassed instruction
                # We modify the already existing instruction
                # This is wrong
                self.instruction.opcode = opcode
                self.instructions[opcode.opcode] = self.instruction
            else:
                # If self.instruction is not set, build a generic one
                self.instructions[opcode.opcode] = Instruction(
                    self.name, opcode, self.description
                )

    def execute(self, cpu, memory):
        "Execute the instruction"
        self.logger.debug("Executing instruction: {}".format(self))

        # TODO
        # self.execute_opcode()

        raise UnimplementedInstruction

    def get_opcode_by_opcode(self, opcode):
        """
        Get by an opcode
        The opcode argument is an integer
        """
        return self.opcodes[opcode]

    def get_instruction_by_opcode(self, opcode):
        """
        Build an Instruction given an opcode
        The opcode argument is an integer
        """
        return self.instructions[opcode]

    def short_str(self):
        return "{}".format(self.name)


@dataclass
class Instructions:
    """
    A set of instructions
    """

    instructions: list[Instruction]

    def __post_init__(self):
        "Create a dictionary so we can access instructions by opcode"
        self.opcode_dict = {}
        for instruction in self.instructions:
            self.opcode_dict[instruction.opcode.opcode] = instruction

    def __iter__(self):
        return iter(self.instructions)

    def get_by_opcode(self, opcode):
        if opcode in self.opcode_dict:
            return self.opcode_dict[opcode]
        else:
            raise UndocumentedInstruction


@dataclass
class InstructionSet:
    """
    The collection of instructions this processor supports
    This is essentially a list of InstructionClasses
    OR it could be a list of Instructions
    """

    instructions: list[InstructionClass]

    def __post_init__(self):
        "Create a dictionary so we can access instructions by opcode"
        self.logger = logging.getLogger("bitey.cpu.instruction.instruction")
        self.opcode_dict = {}
        for instruction in self.instructions:
            for opcode in instruction.opcodes:
                self.opcode_dict[opcode.opcode] = instruction

    def __iter__(self):
        return iter(self.instructions)

    def get_by_opcode(self, opcode):
        if opcode in self.opcode_dict:
            return self.opcode_dict[opcode]
        else:
            raise UndocumentedInstruction

    def get_instruction_by_opcode(self, opcode):
        """
        Get an instruction by its opcode
        """
        if opcode in self.opcode_dict:
            # This isn't good
            # More fail
            # TODO: Rebuild it
            instruction_class = self.opcode_dict[opcode]
            instruction = instruction_class.instruction
            if instruction is None:
                instruction = instruction_class.get_instruction_by_opcode(opcode)
            else:
                instruction.opcode = instruction_class.opcodes[opcode]

            return instruction
        else:
            raise UndocumentedInstruction
