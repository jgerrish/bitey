from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class CLI(Instruction):
    "CLI Clear Interrupt Disable"


    def execute(self, flags, registers, memory):
        "Execute the instruction"
        self.set_flags(flags, registers)
        return

    # Maybe this should be executed by the instruction, not the CPU
    def set_flags(self, flags, registers):
        flags["I"].clear()
        return
