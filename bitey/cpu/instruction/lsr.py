from bitey.cpu.addressing_mode import AccumulatorAddressingMode
from bitey.cpu.instruction.instruction import Instruction, IncompleteInstruction


class LSR(Instruction):
    """
    Right Shift One Bit (Memory or Accumulator)

    Logical Shift Right

    Shift right one bit

    Bit seven is always set to zero.

    The carry flag is set to the original value of bit zero.
    The N flag is always reset.
    The Z flag is set if the new value is zero, other it's reset.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Right Shift One Bit (Memory or Accumulator)

        Logical Shift Right

        Shift right one bit

        Bit seven is always set to zero.

        The carry flag is set to the original value of bit zero.
        The N flag is always reset.
        The Z flag is set if the new value is zero, other it's reset.
        """
        if value is not None:
            if (value & 0x01) != 0:
                cpu.flags["C"].set()
            else:
                cpu.flags["C"].clear()

            self.result = (value >> 1) & 0xFF
            if isinstance(self.opcode.addressing_mode, AccumulatorAddressingMode):
                cpu.registers["A"].set(self.result)
            elif address is not None:
                memory.write(address, self.result)
            else:
                raise IncompleteInstruction

            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)
