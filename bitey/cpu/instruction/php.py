from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class PHP(Instruction):
    """
    PHP: Push Processor Status on Stack

    Push the processor status register onto the stack.
    This updates the stack pointer register to point to the next empty location.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        cpu.stack_push(memory, cpu.registers["P"].get())
