from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction


@dataclass
class ORA(Instruction):
    """
    ORA: ORA Memory with Accumulator
    Perform a bitwise or with the Accumulator ORA a value in memory.
    Store the result in the accumulator.
    Sets the zero flag if the result is zero.
    Sets the negative flag if the result has a one in bit seven.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, bit-wise ORAing the accumulator ORA memory
        """
        if value is not None:
            cpu.registers["A"].set(cpu.registers["A"].get() | value)
            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the ORA.
        Resets the zero flag if the accumulator is not zero as the result of the ORA.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_register_result(registers["A"])
        flags["Z"].test_register_result(registers["A"])
