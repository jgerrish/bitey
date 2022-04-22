from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction, IncompleteInstruction


@dataclass
class BIT(Instruction):
    """
    BIT: Test Bits in Memory with Accumulator

    This instruction bitwise ANDs a value in memory and the accumulator.

    The N flag is set if bit seven of the memory location is set,
    otherwise it is cleared.

    The V flag is set if bit six of the memory location is set,
    otherwise it is cleared.

    The Z flag is set if the result of the AND operation is zero,
    otherwise it is cleared.
    """

    def instruction_execute(self, cpu, memory, value, address):
        "Execute the instruction"
        if value is not None:
            self.value = value
            self.result = cpu.registers["A"].get() & value
            self.set_flags(cpu.flags, cpu.registers)
        else:
            self.value = None
            self.result = None
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        if self.value is not None:
            # The Negative flag is set based on the value in the memory location, not the
            # final result of the AND
            if (self.value & 0x80) != 0x00:
                flags["N"].set()
            else:
                flags["N"].clear()
            # The Overflow flag is set based on the value in the memory location, not them
            # final result of the AND
            if (self.value & 0x40) != 0x00:
                flags["V"].set()
            else:
                flags["V"].clear()

        if self.result is not None:
            if self.result == 0x00:
                flags["Z"].set()
            else:
                flags["Z"].clear()

        return
