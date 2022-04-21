from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BCS(Instruction):
    """
    BCS: Branch on Carry Set

    Branch if the Carry Flag is True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["C"].status is True):
            cpu.registers["PC"].set(address)
