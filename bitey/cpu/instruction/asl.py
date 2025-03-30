from bitey.cpu.instruction.instruction import Instruction
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction


class ASL(Instruction):
    """
    Shift Left One Bit (Memory or Accumulator)

    Shift left one bit

    Bit zero is always set to zero.

    The carry flag is set to the original value of bit seven.
    The N flag is set if the new value of bit seven is one, otherwise
    it's reset.
    The Z flag is set if the new value is zero, other it's reset.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Shift Left One Bit (Memory or Accumulator)

        Bit zero is always set to zero.

        The carry flag is set to the original value of bit seven.
        The N flag is set if the new value of bit seven is one, otherwise
        it's reset.
        The Z flag is set if the new value is zero, other it's reset.
        """
        if value is not None:
            if (value & 0x80) != 0:
                cpu.flags["C"].set()
            else:
                cpu.flags["C"].clear()

            self.result = (value << 1) & 0xFF

            self.opcode.addressing_mode.write(
                cpu.flags, cpu.registers, memory, address, self.result
            )

            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)
