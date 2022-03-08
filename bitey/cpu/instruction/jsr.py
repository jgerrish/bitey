from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


@dataclass
class JSR(Instruction):
    "JSR: Jump to New Location Saving Return Address"

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, saving the current address and jumping to
        the new location
        """
        # We store the next PC address on the stack
        # JSR is always an absolute addressing mode instruction, so it's always three
        # bytes
        if address is not None:
            cpu.stack_push_address(memory, cpu.registers["PC"].get())
            cpu.registers["PC"].set(address)
        else:
            raise IncompleteInstruction
