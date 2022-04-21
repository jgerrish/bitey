from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class BMI(Instruction):
    """
    BMI: Branch on Result Minus

    Branch if the Negative Flag is True
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        if (address is not None) and (cpu.flags["N"].status is True):
            cpu.registers["PC"].set(address)
