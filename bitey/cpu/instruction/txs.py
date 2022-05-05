from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction


@dataclass
class TXS(Instruction):
    """
    TXS Transfer index X to stack pointer

    Changing the value of the stack pointer alone is not enough, we need
    to change the stack start CPU variable too.

    This is based on the semantics of the TXS instruction, it's normal
    use is to setup a new stack, not just to jump around in the
    current stack.

    There are other questions here, there may be cases we don't want
    to change the stack start.  There may be cases we want to set the
    stack pointer to a position in the middle of a page, but keep the
    end of the stack on a page boundary.
    """

    def instruction_execute(self, cpu, memory, value, address):
        "Execute the instruction"
        cpu.stack_init(cpu.registers["X"].get())
