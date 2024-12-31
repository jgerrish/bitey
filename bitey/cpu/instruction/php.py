from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class PHP(Instruction):
    """
    PHP: Push Processor Status on Stack

    Push the processor status register onto the stack.
    This updates the stack pointer register to point to the next empty location.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        # TODO: Describe the reason for the OR with 0b00110000 (the
        # Break and Expansion flags)
        #
        # https://github.com/Klaus2m5/6502_65C02_functional_tests/issues/13
        # http://forum.6502.org/viewtopic.php?f=2&t=2241&hilit=request+for+verification&start=30#p20914
        # https://www.nesdev.org/wiki/Visual6502wiki/6502_BRK_and_B_bit
        cpu.stack_push(memory, cpu.registers["P"].get() | 0x30)

        # set the flags
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        "Set the Reserved and Break flags"
        # Set the Reserved flag
        flags["E"].set()

        # Set the Break flag
        flags["B"].set()
