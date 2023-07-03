from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class TXS(Instruction):
    """
    TXS Transfer index X to stack pointer

    This is simplified from the previous behavior.  We set the stack
    register with the value of the X index register.

    The stack base or start are not changed.
    """

    def instruction_execute(self, cpu, memory, value, address):
        "Execute the instruction"
        cpu.registers["S"].set(cpu.registers["X"].get())
