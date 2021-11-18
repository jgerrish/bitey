from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class TXS(Instruction):
    "TXS Transfer index X to stack pointer"

    def execute(self, registers, memory):
        "Execute the instruction"
        return

    def set_flags(self, flags, registers):
        return
