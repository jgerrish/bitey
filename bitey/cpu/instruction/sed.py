from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class SED(Instruction):
    "SED: Set Decimal Mode"

    def execute(self, cpu, memory):
        "Execute the instruction"
        self.set_flags(cpu.flags, cpu.registers)
        return

    def set_flags(self, flags, registers):
        flags["D"].set()
        return
