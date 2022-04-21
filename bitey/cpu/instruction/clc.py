from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class CLC(Instruction):
    "CLC Clear Carry Flag"

    def execute(self, cpu, memory):
        "Execute the instruction"
        self.set_flags(cpu.flags, cpu.registers)
        return

    def set_flags(self, flags, registers):
        flags["C"].clear()
        return
