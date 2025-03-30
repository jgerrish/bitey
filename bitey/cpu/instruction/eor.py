from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction


@dataclass
class EOR(Instruction):
    """
    EOR: Exclusive Or Memory with Accumulator
    Perform a bitwise exclusive or with the Accumulator and a value in memory.

    The exclusive or is an operation that compares every bit in both the accumulator and
    memory location.  If both bits are the same, the bit is set to zero, if both bits
    are different, the bit is set to one.

    Store the result in the accumulator.
    Sets the zero flag if the result is zero.
    Resets it otherwise.
    Sets the negative flag if the result has a one in bit seven.
    Resets it otherwise.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, bit-wise eoring the accumulator and memory
        """
        if value is not None:
            cpu.registers["A"].set(cpu.registers["A"].get() ^ value)
            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the EOR.
        Resets the zero flag if the accumulator is not zero as the result of the EOR.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_register_result(registers["A"])
        flags["Z"].test_register_result(registers["A"])
