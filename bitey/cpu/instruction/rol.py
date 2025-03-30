from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class ROL(Instruction):
    """
    ROL: Rotate One Bit Left (Memory or Accumulator)
    Rotate one bit left.

    Stores the carry in the carry flag.
    Store the carry flag in bit zero.

    ROL is a read/modify/write instructon, so it stores the result in
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

            # Set the carry flag based on the highest bit
            if (value & 0b10000000) != 0:
                cpu.flags["C"].set()
            else:
                cpu.flags["C"].clear()

            # rotate left one bit
            self.result <<= 1
            self.result &= 0xFF

            # set the first bit if the old status of the carry flag was set
            self.result |= 1 if carry else 0

            self.set_flags(cpu.flags, cpu.registers)

        # TODO: Some of the instructions have this inside the "value is not None" check, some
        # don't.  Fix it and make it consistent.
        self.opcode.addressing_mode.write(
            cpu.flags, cpu.registers, memory, address, self.result
        )

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the EOR.
        Resets the zero flag if the accumulator is not zero as the result of the EOR.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)
