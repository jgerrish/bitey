from dataclasses import dataclass
from bitey.cpu.instruction.opcode import Opcodes


@dataclass
class Instruction:
    """
    A CPU instruction
    """

    # TODO: Extend to allow multiple opcodes and addressing modes

    name: str
    "The name of the instruction"

    opcodes: Opcodes
    "The instruction opcodes"

    description: str
    "A human-readable description of the instruction"


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

    def get_by_opcode(self, opcode):
        return self.opcode_dict[opcode]
