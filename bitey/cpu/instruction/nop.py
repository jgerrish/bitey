from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class NOP(Instruction):
    """
    BNE: No Operation
    Doesn't do anything
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        return
