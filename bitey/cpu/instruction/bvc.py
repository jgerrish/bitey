from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BVC(Instruction):
    """
    BVC: Branch on Overflow Clear

    Branch if the Overflow Flag is not True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["V"].status is not True):
            cpu.registers["PC"].set(address)
