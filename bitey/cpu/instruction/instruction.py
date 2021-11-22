from dataclasses import dataclass
import logging
from bitey.cpu.instruction.opcode import Opcodes


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

    opcodes: Opcodes
    "The instruction opcodes"

    description: str
    "A human-readable description of the instruction"

    def __post_init__(self):
        self.logger = logging.getLogger("bitey")

    def execute(self, cpu, memory):
        "Execute the instruction"
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

        # TODO
        # self.execute_opcode()

        raise UnimplementedInstruction

    def get_opcode(self, opcode):
        return self.opcodes[opcode]

    def short_str(self):
        return "{}".format(self.name)


@dataclass
class Instructions:
    """
    The collection of instructions this processor supports
    """

    instructions: list[Instruction]

    def __post_init__(self):
        "Create a dictionary so we can access instructions by opcode"
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
