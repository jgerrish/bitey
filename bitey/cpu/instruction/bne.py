from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BNE(Instruction):
    """
    BNE: Branch on Result Plus
    Also known on Branch if Not Equal
    Branch if the Zero Flag is not True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if cpu.flags["Z"].status is not True:
            cpu.registers["PC"].set(value)
