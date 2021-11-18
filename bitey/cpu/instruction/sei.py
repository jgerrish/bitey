from dataclasses import dataclass
#from bitey.cpu.cpu import CPU
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class SEI(Instruction):
    "SEI: Set Interrupt Disable"

    def execute(self, flags, registers, memory):
        "Execute the instruction"
        self.set_flags(flags, registers)
        return

    # Maybe this should be executed by the instruction, not the CPU
    def set_flags(self, flags, registers):
        flags["I"].set()
        return
