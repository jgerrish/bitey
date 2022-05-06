from bitey.cpu.instruction.instruction import Instruction, IncompleteInstruction

# from bitey.cpu.arch import EightBitArch


class CP(Instruction):
    """
    Generic register-independent compare instruction

    Subtract the contents of memory from the contents of the index.
    Then test flags based on that result.

    The zero flag is set when the register and memory are equal
    The carry flag is set when the value in memory is less than or equal to the register
    The negative flag is set when memory is greater than the register
    """

    def __init__(self, name, opcode, description, options, register):
        "Initialize with the register"
        super().__init__(name, opcode, description, options)
        self.register = register
        # result is the intermediate result of the subtraction
        self.result = None

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Subtract the contents of memory from the contents of the index
        Store the intermediate result, then test flags.

        From the MCS6500 Family Programming Manual,
        the results of a compare are:

                                 N           C        Z          V
        Accumulator < Memory    Either     Reset    Reset    Unchanged
        Accumulator = Memory    Reset       Set      Set     Unchanged
        Accumulator > Memory    Either      Set     Reset    Unchanged
        """
        if value is not None:
            self.value = value
            self.register_value = cpu.registers[self.register].get()

            # Using simple subtraction
            self.result = self.register_value - self.value

            # Using proper two's complement addition for subtraction
            # self.complemented_value = 0xFF - self.value
            # self.result = 0xFF - (self.register_value + self.complemented_value)
            # # self.result = EightBitArch.signed_int_to_twos_complement(result)

            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        if self.register_value < self.value:
            flags["C"].clear()
        else:
            flags["C"].set()
        flags["N"].test_result(self.result)
        flags["Z"].test_result(self.result)


class CMP(CP):
    """
    Compare Memory and Accumulator
    """

    def __init__(self, name, opcode, description, options):
        super().__init__(name, opcode, description, options, "A")


class CPX(CP):
    """
    Compare Memory and Index X
    """

    def __init__(self, name, opcode, description, options):
        super().__init__(name, opcode, description, options, "X")


class CPY(CP):
    """
    Compare Memory and Index Y
    """

    def __init__(self, name, opcode, description, options):
        super().__init__(name, opcode, description, options, "Y")
