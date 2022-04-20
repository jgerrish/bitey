from bitey.cpu.instruction.instruction import Instruction


class TAU(Instruction):
    "Generic transfer accumulator to index instruction"

    def __init__(self, name, opcode, description, options, register):
        "Initialize with the register"
        super().__init__(name, opcode, description, options)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        "Execute the instruction, storing the accumulator value into the register"
        self.result = cpu.registers["A"].get()
        cpu.registers[self.register].set(self.result)
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)


class TAX(TAU):
    "TAX: Transfer Accumulator to Index X"

    def __init__(self, name, opcode, description, options=None):
        super().__init__(name, opcode, description, options, "X")


class TAY(TAU):
    "TAY: Transfer Accumulator to Index Y"

    def __init__(self, name, opcode, description, options=None):
        super().__init__(name, opcode, description, options, "Y")


class TUA(Instruction):
    "Generic transfer index to accumulator instruction"

    def __init__(self, name, opcode, description, options, register):
        "Initialize with the register"
        super().__init__(name, opcode, description, options)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        "Execute the instruction, storing the register value into the accumulator"
        self.result = cpu.registers[self.register].get()
        cpu.registers["A"].set(self.result)
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)


class TXA(TUA):
    "TAX: Transfer Index X to Accumulator"

    def __init__(self, name, opcode, description, options=None):
        super().__init__(name, opcode, description, options, "X")


class TYA(TUA):
    "TAY: Transfer Index Y to Accumulator"

    def __init__(self, name, opcode, description, options=None):
        super().__init__(name, opcode, description, options, "Y")
