from dataclasses import dataclass
from typing import ClassVar
from bitey.cpu.instruction.instruction import Instruction


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

    def instruction_execute(self, cpu, memory, value=None, address=None):
        "Execute the instruction"

        # Set the Break (B) flag to indicate this interrupt was caused
        # by a BRK instruction.
        # TODO: It's ambigous how to do this, whether the interrupt
        # handler has to pop the flags, check the B bit, and
        # push it back on the stack or if there should be two stack
        # pushes for the P register
        # Since the manual says the value is invalid while not in an
        # interrupt handling routine, we'll let the BRK and hw interrupts
        # always manage it before a call
        self.set_flags(cpu.flags, cpu.registers)

        # super().execute(cpu, memory)
        # Push the instruction after the next on the stack
        pc = cpu.registers["PC"].get()
        cpu.stack_push_address(memory, pc)

        # save all the flags on the stack
        cpu.stack_push(memory, cpu.registers["P"].get() & 0xFF)

        # Push the break flag on the top of the stack so the interrupt
        # handler can process it
        # bit_field_pos = cpu.flags["B"].bit_field_pos
        # cpu.stack_push(memory, cpu.flags.data & (2 ** bit_field_pos))

        # Get the interrupt vector
        (al, ah) = BRK.maskable_interrupt_vector
        address = memory.get_16bit_value(al, ah)

        cpu.registers["PC"].set(address)

    def set_flags(self, flags, registers):
        "Set the Interrupt Disable and Break flags"

        # Set the Interrupt Disable flag to disable interrupts
        flags["I"].set()

        # Set the Break flag to indicate a software interrupt
        flags["B"].set()
