from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
)


@dataclass
class LDX(Instruction):
    "LDX Load X with memory"

    def execute(self, flags, registers, memory):
        "Execute the instruction"
        # TODO: Implment this
        # value = self.addressing_mode.get_value(memory)
        # registers["X"].value = value
        self.set_flags(flags, registers)

        return

    # Maybe this should be executed by the instruction, not the CPU
    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["X"])
        return
