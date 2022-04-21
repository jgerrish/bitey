from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BCC(Instruction):
    """
    BCC: Branch on Carry Clear

    Branch if the Carry Flag is not True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["C"].status is not True):
            cpu.registers["PC"].set(address)
