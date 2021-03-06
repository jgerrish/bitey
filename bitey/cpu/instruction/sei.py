from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class SEI(Instruction):
    "SEI: Set Interrupt Disable"

    def execute(self, cpu, memory):
        "Execute the instruction"
        self.set_flags(cpu.flags, cpu.registers)
        return

    def set_flags(self, flags, registers):
        flags["I"].set()
        return
