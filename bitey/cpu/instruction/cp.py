from bitey.cpu.instruction.instruction import Instruction, IncompleteInstruction
from bitey.cpu.arch import EightBitArch


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
        """
        if value is not None:
            result = cpu.registers[self.register].get() - value
            self.result = EightBitArch.signed_int_to_twos_complement(result)
            # logger.debug("register: {}, memory: {}, result: {}")
            self.set_flags(cpu.flags, cpu.registers)
        else:
            raise IncompleteInstruction

    def set_flags(self, flags, registers):
        """
        Sets flags based on the result of the subtract operation
        """
        flags["C"].test_result(self.result)
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
