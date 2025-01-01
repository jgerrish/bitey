from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class RTI(Instruction):
    """
    RTI: Return from Interrupt

    Return from an Interrupt

    Restore the return address from the stack so we can return from the interrupt.
    """

    def instruction_execute(self, cpu, memory, value=None, address=None):
        "RTI: Return from Interrupt"

        # The interrupt stores the flag data on top of the stack
        cpu.registers["P"].set(cpu.stack_pop(memory))

        # Set flags
        self.set_flags(cpu.flags, cpu.registers)

        # The interrupt stores the return address after the flag data
        cpu.registers["PC"].set(cpu.stack_pop_address(memory))

    def set_flags(self, flags, registers):
        "Set and clear relevant flags"
        flags["E"].set()
        flags["B"].clear()
