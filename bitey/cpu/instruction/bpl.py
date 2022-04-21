from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BPL(Instruction):
    """
    BPL: Branch on Result Plus

    Branch if the Negative Flag is not True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["N"].status is not True):
            cpu.registers["PC"].set(address)
