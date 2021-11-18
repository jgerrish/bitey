from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class STA(Instruction):
    "STA: Store Accumulator"

