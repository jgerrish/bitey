from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BEQ(Instruction):
    """
    BEQ: Branch on Result Zero
    Also known on Branch if Equal
    Branch if the Zero Flag is True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if cpu.flags["Z"].status is True:
            cpu.registers["PC"].set(value)
