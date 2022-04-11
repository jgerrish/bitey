from dataclasses import dataclass
from bitey.cpu.addressing_mode import AccumulatorAddressingMode
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class ROR(Instruction):
    """
    ROR: Rotate One Bit Right (Memory or Accumulator)
    Rotate one bit right.

    Stores the carry in the carry flag.
    Store the carry flag in bit seven.

    ROR is a read/modify/write instructon, so it stores the result in
    the memory if it is used with a memory-based addressing mode.

    Sets the zero flag if the result is zero.
    Resets it otherwise.
    Sets the negative flag if the result has a one in bit seven.
    Resets it otherwise.
    Does not affect the overflow flag.

    Some earlier versions of the 6502 were bugged and the ROR instruction
    did not change the carry bit.  This version does not have that bug.

    Setting the bugged flag to True will enable this buggy behavior.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, bit-wise eoring the accumulator and memory
        """
        if value is not None:
            self.result = value
            carry = cpu.flags["C"].status

            # Set the carry flag based on the highest bit
            if (value & 0b00000001) != 0:
                cpu.flags["C"].set()
            else:
                cpu.flags["C"].clear()

            # rotate right one bit
            self.result >>= 1

            # set the highest bit if the old status of the carry flag was set
            self.result |= 0x80 if carry else 0x00

            self.set_flags(cpu.flags, cpu.registers)

        if type(self.opcode.addressing_mode) == AccumulatorAddressingMode:
            cpu.registers["A"].set(self.result)
        elif address is not None:
            memory.write(address, self.result)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the EOR.
        Resets the zero flag if the accumulator is not zero as the result of the EOR.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)


class RORNoCarryBug(Instruction):
    """
    ROR: Rotate One Bit Right (Memory or Accumulator)
    Rotate one bit right.

    This has a quirk where the carry flag is not set if there is a carry

    ROR is a read/modify/write instructon, so it stores the result in
    the memory if it is used with a memory-based addressing mode.

    Sets the zero flag if the result is zero.
    Resets it otherwise.
    Sets the negative flag if the result has a one in bit seven.
    Resets it otherwise.
    Does not affect the overflow flag.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, bit-wise eoring the accumulator and memory
        """
        if value is not None:
            self.result = value
            carry = cpu.flags["C"].status

            # rotate right one bit
            self.result >>= 1

            # set the highest bit if the old status of the carry flag was set
            self.result |= 0x80 if carry else 0x00

            self.set_flags(cpu.flags, cpu.registers)

        if type(self.opcode.addressing_mode) == AccumulatorAddressingMode:
            cpu.registers["A"].set(self.result)
        elif address is not None:
            memory.write(address, self.result)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the EOR.
        Resets the zero flag if the accumulator is not zero as the result of the EOR.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)
