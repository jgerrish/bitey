from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class RTS(Instruction):
    "RTS: Return from Subroutine"

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, getting the return address from the stack
        and jumping there.
        """
        cpu.registers["PC"].set(cpu.stack_pop_address(memory))
