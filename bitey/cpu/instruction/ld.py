from bitey.cpu.instruction.instruction import (
    IncompleteInstruction,
    Instruction,
)


class LD(Instruction):
    "Generic load register with memory instruction"

    def __init__(self, name, opcode, description, options={}, register=None):
        "Initialize with the register"
        super().__init__(name, opcode, description, options)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        "Execute the instruction, loading the register with a memory value"
        if value is not None:
            cpu.registers[self.register].set(value)
            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Set the zero flag if the accumulator is zero as the result of the LD.
        Resets the zero flag if the accumulator is not zero as the result of the LD.
        Sets the negative (N) flag if bit 7 is one.
        """
        flags["N"].test_register_result(registers[self.register])
        flags["Z"].test_register_result(registers[self.register])


class LDA(LD):
    "LDA: Load Accumulator with Memory"

    def __init__(self, name, opcode, description, options={}):
        super().__init__(name, opcode, description, options, "A")


class LDX(LD):
    "LDX: Load Index X with Memory"

    def __init__(self, name, opcode, description, options={}):
        super().__init__(name, opcode, description, options, "X")


class LDY(LD):
    "LDA: Load Index Y with Memory"

    def __init__(self, name, opcode, description, options={}):
        super().__init__(name, opcode, description, options, "Y")
