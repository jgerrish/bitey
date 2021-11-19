from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    UntestedInstruction,
)


@dataclass
class LDX(Instruction):
    "LDX Load X with memory"

    def execute(self, cpu, memory):
        "Execute the instruction"
        raise UntestedInstruction

        value = self.addressing_mode.get_value(memory)
        cpu.registers["X"].value = value
        self.set_flags(cpu.flags, cpu.registers)

        return

    # Maybe this should be executed by the instruction, not the CPU
    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["X"])
        return
