from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


class IN(Instruction):
    "Generic register increment instruction"

    def __init__(self, name, opcode, description, options, register):
        "Initialize with the register"
        super().__init__(name, opcode, description, options)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, incrementing the register by one.
        """
        cpu.registers[self.register].inc()
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        flags["N"].test_register_result(registers[self.register])
        flags["Z"].test_register_result(registers[self.register])


class INX(IN):
    "INX: Increment Index X by One"

    def __init__(self, name, opcode, description, options):
        super().__init__(name, opcode, description, options, "X")


class INY(IN):
    "INY: Increment Index Y by One"

    def __init__(self, name, opcode, description, options):
        super().__init__(name, opcode, description, options, "Y")


class INC(Instruction):
    "Incrementy Memory by One"

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, incrementing the register by one.
        """
        if value is not None:
            value = (value + 1) & 0xFF
            memory.write(address, value)
            self.set_flags(cpu.flags, cpu.registers, value)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers, value):
        flags["N"].test_result(value)
        flags["Z"].test_result(value)
