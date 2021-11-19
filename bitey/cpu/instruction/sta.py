from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    UnimplementedInstruction,
)


@dataclass
class STA(Instruction):
    "STA: Store Accumulator"

    def execute(self, cpu, memory):
        raise UnimplementedInstruction
