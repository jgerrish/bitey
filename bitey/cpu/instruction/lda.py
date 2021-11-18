from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class LDA(Instruction):
    "LDA: Load Accumulator"


    def execute(self, registers, memory):
        "Execute the instruction"
        set_flags()

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["A"])
