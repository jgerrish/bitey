from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)


class DE(Instruction):
    "Generic register decrement instruction"

    def __init__(self, name, opcode, description, register):
        "Initialize with the register"
        super().__init__(name, opcode, description)
        self.register = register

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, decrementing the register by one.
        """
        cpu.registers[self.register].dec()
        self.set_flags(cpu.flags, cpu.registers)

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers[self.register])


class DEX(DE):
    "DEX: Decrement Index X by One"

    def __init__(self, name, opcode, description):
        super().__init__(name, opcode, description, "X")


class DEY(DE):
    "DEY: Decrement Index Y by One"

    def __init__(self, name, opcode, description):
        super().__init__(name, opcode, description, "Y")


class DEC(Instruction):
    "Decrement Memory by One"

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, incrementing the register by one.
        """
        if value is not None:
            value = value - 1
            if value < 0:
                value = 0xFF
            memory.write(address, value)
            self.set_flags(cpu.flags, cpu.registers, value)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers, value):
        # The zero flag is set when the value is zero, not necessarily on a wrap
        if value == 0x00:
            flags["Z"].set()
