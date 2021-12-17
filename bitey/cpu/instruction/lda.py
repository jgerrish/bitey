from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class LDA(Instruction):
    "LDA: Load Accumulator"

    def execute(self, cpu, memory):
        "Execute the instruction"
        raise IncompleteInstruction
        # self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["A"])
