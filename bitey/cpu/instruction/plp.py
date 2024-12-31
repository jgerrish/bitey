from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class PLP(Instruction):
    """
    PLP: Pull Processor Status from Stack

    Pop the processor status register from the top of the stack.
    This updates the stack pointer register.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        cpu.registers["P"].set(cpu.stack_pop(memory))

        # Set flags
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        "Set the flags"
        flags["E"].set()
        flags["B"].clear()
