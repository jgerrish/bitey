from dataclasses import dataclass
from typing import ClassVar
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class BRK(Instruction):
    """
    BRK: Force Break

    Simulate an interrupt.

    Store the second byte after the BRK command on the stack
    so we can return from the interrupt.

    BRK cannot be masked by setting the I flag.
    """

    maskable_interrupt_vector: ClassVar[tuple] = (0xFFFE, 0xFFFF)
    "The location in memory storing the interrupt vector routine address"

    def execute(self, cpu, memory):
        "Execute the instruction"

        # super().execute(cpu, memory)
        # Push the instruction after the next on the stack
        pc = cpu.registers["PC"].value
        cpu.stack_push_address(memory, pc + 2)

        self.set_flags(cpu.flags, cpu.registers)

        # save the break command flag on the stack
        cpu.stack_push(memory, cpu.flags.data)

        # Get the interrupt vector
        (al, ah) = BRK.maskable_interrupt_vector
        memory.get_16bit_value(al, ah)

        raise IncompleteInstruction
        # TODO: There is ambiguity in the manual about whether the B flag
        # is reset at the end of the instruction

        return

    def set_flags(self, flags, registers):
        "Set any flags as a result of the instruction execution"
        # Set the B flag
        flags["B"].set()
        return
