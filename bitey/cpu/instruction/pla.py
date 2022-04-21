from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class PLA(Instruction):
    """
    PLA: Pull Accumulator from Stack

    Pop the accumulator from the top of the stack.
    This updates the stack pointer register.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        cpu.registers["A"].set(cpu.stack_pop(memory))
