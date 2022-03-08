from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class JMP(Instruction):
    "JMP: Jump to New Location"

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, jumping to the new location
        """
        if address is not None:
            cpu.registers["PC"].set(address)
        else:
            raise IncompleteInstruction
