from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    UnimplementedInstruction,
)


@dataclass
class TXS(Instruction):
    "TXS Transfer index X to stack pointer"

    def execute(self, cpu, memory):
        "Execute the instruction"
        raise UnimplementedInstruction
        return

    def set_flags(self, flags, registers):
        return
