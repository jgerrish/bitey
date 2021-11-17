from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class LDA(Instruction):
    "The instruction opcode"
    opcode: 173
