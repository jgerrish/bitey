from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class LDA(Instruction):
    "LDA: Load Accumulator"

    def instruction_execute(self, cpu, memory, value):
        "Execute the instruction, load the accumulator with the value"
        if value is not None:
            cpu.registers["A"].set(value)
            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["A"])
