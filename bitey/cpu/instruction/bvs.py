from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BVS(Instruction):
    """
    BVS: Branch on Overflow Set

    Branch if the Overflow Flag is True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["V"].status is True):
            cpu.registers["PC"].set(address)
