from dataclasses import dataclass


@dataclass
class AddressingMode:
    """
    Addressing mode base class
    """


class ImpliedAddressingMode(AddressingMode):
    """
    Implied addressing mode
    The address is encoded in the instruction
    """

    def get_value(self, flags, registers, memory):
        return None


class ImmediateAddressingMode(AddressingMode):
    """
    Immediate addressing mode
    The value is encoded as a constant in the next byte
    """

    def get_value(self, flags, registers, memory):
        byte = memory.read(registers["PC"].value)
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].value += 1

        return byte


class ZeroPageAddressingMode(AddressingMode):
    """
    Zero Page addressing mode
    The address in Zero Page is encoded as a constant in the next byte
    """

    def get_value(self, flags, registers, memory):
        address = memory.read(registers["PC"].value)
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].value += 1

        # TODO: Create exception API
        assert address <= 0xFF
        return memory.read(address)


@dataclass
class AbsoluteAddressingMode(AddressingMode):
    """
    Absolute addressing mode
    Absolute addressing is a three-byte instruction
    The address is encoded in the next two bytes after the opcode
    The first byte contains the opcode
    The second byte contains the low-order byte of the effective address
    The effective address contains the data
    The third byte contains the high-order byte of the effective address
    """

    "The low-order byte"
    adl: int = 0

    "The high-order byte"
    adh: int = 0

    def get_value(self, flags, registers, memory):
        self.adl = memory.read(registers["PC"].value)
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].value += 1
        self.adh = memory.read(registers["PC"].value)
        registers["PC"].value += 1

        return memory.read(memory.get_16bit_address(self.adl, self.adh))
