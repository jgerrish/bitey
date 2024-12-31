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
        value = cpu.stack_pop(memory)

        cpu.registers["A"].set(value)

        # set the flags
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the A register is zero as the
        result of the PLA.

        Resets the zero flag if the A register is not zero as
        the result of the PLA.

        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_register_result(registers["A"])
        flags["Z"].test_register_result(registers["A"])
