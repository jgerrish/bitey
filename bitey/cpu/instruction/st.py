from bitey.cpu.instruction.instruction import (
    IncompleteInstruction,
    Instruction,
)


class ST(Instruction):
    "Generic store register in memory instruction"

    def __init__(self, name, opcode, description, register):
        "Initialize with the register"
        super().__init__(name, opcode, description)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        "Execute the instruction, storing the register value into memory"
        if address is not None:
            memory.write(address, cpu.registers[self.register].get())
        else:
            raise IncompleteInstruction


class STA(ST):
    "STA: Store Accumulator in Memory"

    def __init__(self, name, opcode, description):
        super().__init__(name, opcode, description, "A")


class STX(ST):
    "STX: Store Index X in Memory"

    def __init__(self, name, opcode, description):
        super().__init__(name, opcode, description, "X")


class STY(ST):
    "STA: Store Index Y in Memory"

    def __init__(self, name, opcode, description):
        super().__init__(name, opcode, description, "Y")
