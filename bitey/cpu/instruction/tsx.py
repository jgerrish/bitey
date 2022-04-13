from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class TSX(Instruction):
    """
    TSX: Transfer Stack Pointer to Index X

    Transfers the value in the stack pointer to index register X.

    Sets the zero flag if the result is zero, otherwise it's reset.
    Sets the negative flag if the result has a one in bit seven.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, setting the value of the index register X
        to the value of the stack pointer register.
        """
        cpu.registers["X"].set(cpu.registers["S"].get())
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the TSX.
        Resets the zero flag if the accumulator is not zero as the result of the TSX.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_register_result(registers["X"])
        flags["Z"].test_register_result(registers["X"])
