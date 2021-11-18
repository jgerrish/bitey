from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class LDA(Instruction):
    "LDA: Load Accumulator"

    def execute(self, flags, registers, memory):
        "Execute the instruction"
        self.set_flags(flags, registers)

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["A"])
