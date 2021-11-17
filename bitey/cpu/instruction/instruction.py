from dataclasses import dataclass
from bitey.cpu.addressing_mode import AddressingMode


@dataclass
class Instruction:
    """
    A CPU instruction
    """

    "The name of the instruction"
    name: str

    "The instruction opcode"
    opcode: str

    "The instruction addressing mode"
    addressing_mode: AddressingMode

    "A human-readable description of the instruction"
    description: str


@dataclass
class Instructions:
    """
    The collection of instructions this processor supports
    """

    instructions: list[Instruction]

    def __post_init__(self):
        "Create a dictionary so we can access registers by opcode"
        self.opcode_dict = {}
        for i in self.instructions:
            self.opcode_dict[i.opcode] = i

    def get_by_opcode(self, opcode):
        return self.opcode_dict[opcode]
