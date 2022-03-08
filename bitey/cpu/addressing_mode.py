from dataclasses import dataclass
import logging
from typing import ClassVar


@dataclass
class AddressingMode:
    """
    Addressing mode base class
    """

    bytes: int
    """
    The number of bytes an instruction with this addressing mode takes,
    including the instruction itself.
    """

    def __post_init__(self):
        self.logger = logging.getLogger("bitey.cpu.addressing_mode")

    def get_value(self, flags, registers, memory):
        """
        Get the value at the address
        Returns a tuple of the address and value for convenience
        """
        return (None, None)

    def get_address(self, flags, registers, memory):
        """
        Return the effective address
        """
        # The size to consume is bytes minus one for the opcode itself

        size = self.bytes - 1
        if size > 0:
            registers["PC"].add(size)
        return None

    def get_inst_str(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        if address is not None:
            return "${0:02x}".format(address)
        else:
            return ""


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


    The following absolute JMP command would jump to the NOP instruction

    0x0000  0x4C  JMP
    0x0001  0x12
    0x0002  0x34
    ...
    0x3412  NOP
    """

    adl: int = 0
    "The low-order byte"

    adh: int = 0
    "The high-order byte"

    bytes: ClassVar[int] = 3

    def get_address(self, flags, registers, memory):
        self.adl = memory.read(registers["PC"].get())
        registers["PC"].inc()
        self.adh = memory.read(registers["PC"].get())
        registers["PC"].inc()

        return memory.get_16bit_address(self.adl, self.adh)

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        # address = self.get_address(flags, registers, memory)
        address = self.get_address(flags, registers, memory)
        self.logger.debug("AbsoluteAddressing get_value address: {}".format(address))
        if address is not None:
            return "${0:04x}".format(address)
        else:
            return ""


@dataclass
class AccumulatorAddressingMode(AddressingMode):
    """
    Accumulator Addressing Mode
    The address comes from the accumulator
    """

    bytes: ClassVar[int] = 1

    def get_address(self, flags, registers, memory):
        address = registers["A"].get()

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        self.get_address(flags, registers, memory)
        return ""


@dataclass
class AbsoluteIndirectAddressingMode(AddressingMode):
    bytes: ClassVar[int] = 3

    """
    Absolute Indirectaddressing mode
    Absolute Indirect addressing is a three-byte instruction
    The address is encoded in the next two bytes after the opcode
    The first byte contains the opcode
    The second byte contains the low-order byte of an address
    that contains the effective address
    The third byte contains the high-order byte of an address that contains
    the effective address
    The effective address points to the actual location


    The following absolute indirect JMP command would jump to the NOP instruction

    0x0000  0x6C  JMP
    0x0001  0x12
    0x0002  0x34
    ...
    0x3412  0x15
    0x3413  0x34
    ...
    0x3415  0xEA  NOP
    """

    adl: int = 0
    "The low-order byte"

    adh: int = 0
    "The high-order byte"

    bytes: ClassVar[int] = 3

    def get_address(self, flags, registers, memory):
        self.adl = memory.read(registers["PC"].get())
        registers["PC"].inc()
        self.adh = memory.read(registers["PC"].get())
        registers["PC"].inc()

        address_to_address = memory.get_16bit_address(self.adl, self.adh)
        self.adl = memory.read(address_to_address)
        self.adh = memory.read(address_to_address + 1)
        effective_address = memory.get_16bit_address(self.adl, self.adh)
        return effective_address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        if address is not None:
            return "(${0:04x})".format(address)
        else:
            return ""


@dataclass
class AbsoluteXAddressingMode(AddressingMode):
    bytes: ClassVar[int] = 3
    """
    Absolute,X addressing mode
    Absolute addressing is a three-byte instruction
    The address is encoded in the next two bytes after the opcode
    The first byte contains the opcode
    The second byte contains the low-order byte of the effective address
    The effective address contains the data
    The third byte contains the high-order byte of the effective address

    The X Index is then added to this address
    """

    adl: int = 0
    """
    The low-order byte
    This does not include the X offset
    """

    adh: int = 0
    """
    The high-order byte
    This does not include the X offset
    """

    bytes: ClassVar[int] = 3

    def get_address(self, flags, registers, memory):
        self.adl = memory.read(registers["PC"].get())
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].inc()
        self.adh = memory.read(registers["PC"].get())
        registers["PC"].inc()

        address = memory.get_16bit_address(self.adl, self.adh)
        address += registers["X"].get()

        # Wrap at end of memory
        address = address % 0xFFFF

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        # address = self.get_address(flags, registers, memory)
        address = self.get_address(flags, registers, memory)
        if address is not None:
            return "${0:04x},X".format(memory.get_16bit_address(self.adl, self.adh))
        else:
            return ""


@dataclass
class AbsoluteYAddressingMode(AddressingMode):
    bytes: ClassVar[int] = 3
    """
    Absolute,Y addressing mode
    Absolute,Y addressing is a three-byte instruction
    The address is encoded in the next two bytes after the opcode
    The first byte contains the opcode
    The second byte contains the low-order byte of the effective address
    The effective address contains the data
    The third byte contains the high-order byte of the effective address

    The Y Index is then added to this address
    """

    adl: int = 0
    """
    The low-order byte
    This does not include the X offset
    """

    adh: int = 0
    """
    The high-order byte
    This does not include the X offset
    """

    bytes: ClassVar[int] = 3

    def get_address(self, flags, registers, memory):
        self.adl = memory.read(registers["PC"].get())
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].inc()
        self.adh = memory.read(registers["PC"].get())
        registers["PC"].inc()

        address = memory.get_16bit_address(self.adl, self.adh)
        address += registers["Y"].get()

        # Wrap at end of memory
        address = address % 0xFFFF

        return address

    def get_value(self, flags, registers, memory):
        return memory.read(self.get_address(flags, registers, memory))

    def get_inst_str(self, flags, registers, memory):
        # address = self.get_address(flags, registers, memory)
        address = self.get_address(flags, registers, memory)
        if address is not None:
            return "${0:04x},Y".format(memory.get_16bit_address(self.adl, self.adh))
        else:
            return ""


@dataclass
class ImmediateAddressingMode(AddressingMode):
    """
    Immediate addressing mode
    The value is encoded as a constant in the next byte
    """

    bytes: ClassVar[int] = 2

    def get_value(self, flags, registers, memory):
        byte = memory.read(registers["PC"].get())
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        registers["PC"].inc()

        return (None, byte)

    def get_inst_str(self, flags, registers, memory):
        (address, value) = self.get_value(flags, registers, memory)
        return "#${0:02x}".format(value)


@dataclass
class ImpliedAddressingMode(AddressingMode):
    """
    Implied addressing mode
    The address is encoded in the instruction
    """

    bytes: ClassVar[int] = 1

    def get_address(self, flags, registers, memory):
        return None

    def get_value(self, flags, registers, memory):
        return (None, None)


@dataclass
class IndexedIndirectAddressingMode(AddressingMode):
    """
    Indexed Indirect addressing mode
    Get an address in zero page memory from the next byte and the Z Index.
    The Z index is added to the base address before fetching the effective
    address.  This is different than Indirect Indexed, where the Index
    is added after fetching the address from Zero Page.
    Also called Indirect X
    A1 80  LDA ($80,X)
    """

    bytes: ClassVar[int] = 2

    def get_address(self, flags, registers, memory):
        zero_page_address = registers["PC"].get()
        registers["PC"].inc()

        zero_page_address += registers["X"].get()
        # verify wrapping is the correct behavior
        zero_page_address = zero_page_address % 0xFF

        adl = zero_page_address
        # TODO: Test for case we go beyond the page boundary
        # Wraparound is assumed
        adh = zero_page_address + 1
        address = memory.get_16bit_value(adl, adh)

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)

        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        self.get_address(flags, registers, memory)
        return "(${0:02x},X)".format(address)


@dataclass
class IndirectIndexedAddressingMode(AddressingMode):
    """
    Indirect Indexed addressing mode.
    Get an address in zero page memory from the next byte.
    The address in zero page is two bytes long.  The first byte is the
    low-order byte.  The second is the high-order byte.
    It then adds the Y Index to this address.
    Also called Indirect Y
    B1 80  LDA ($80),Y
    """

    bytes: ClassVar[int] = 2

    def get_address(self, flags, registers, memory):
        zero_page_address = registers["PC"].get()
        registers["PC"].inc()

        adl = zero_page_address
        # TODO: Test for case we go beyond the page boundary
        # Wrap-around is assumed
        adh = zero_page_address + 1

        address = memory.get_16bit_value(adl, adh)
        address += registers["Y"].get()

        # TODO: Verify wrapping is the correct behavior
        address = address % 0xFFFF

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)

        return (address, memory.read(address))

    def get_inst_str(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        self.get_address(flags, registers, memory)
        return "(${0:02x}),Y".format(address)


@dataclass
class IndirectXAddressingMode(AddressingMode):
    """
    Another name for Indexed Indirect Addressing
    TODO: Maybe consolidate these
    """

    bytes: ClassVar[int] = 2

    def __post_init__(self):
        self.am = IndexedIndirectAddressingMode()

    def get_address(self, flags, registers, memory):
        return self.am.get_address(flags, registers, memory)

    def get_value(self, flags, registers, memory):
        return (self, self.am.get_value(flags, registers, memory))

    def get_inst_str(self, flags, registers, memory):
        return self.am.get_inst_str(flags, registers, memory)


@dataclass
class IndirectYAddressingMode(AddressingMode):
    """
    Another name for Indirect Indexed Addressing
    TODO: Maybe consolidate these
    """

    bytes: ClassVar[int] = 2

    def __post_init__(self):
        self.am = IndirectIndexedAddressingMode()

    def get_address(self, flags, registers, memory):
        return self.am.get_address(flags, registers, memory)

    def get_value(self, flags, registers, memory):
        return self.am.get_value(flags, registers, memory)

    def get_inst_str(self, flags, registers, memory):
        return self.am.get_inst_str(flags, registers, memory)


@dataclass
class ZeroPageAddressingMode(AddressingMode):
    """
    Zero Page addressing mode
    The address in Zero Page is encoded as a constant in the next byte
    """

    bytes: ClassVar[int] = 2

    def get_address(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        registers["PC"].inc()

        # TODO: Create exception API
        assert address <= 0xFF

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)
        return (address, memory.read(address))


@dataclass
class ZeroPageXAddressingMode(AddressingMode):
    """
    Zero Page X addressing mode
    Compute the address by adding the value the PC points to
    plus the X register value.
    Wraps if the value is greater than 0x255.
    """

    bytes: ClassVar[int] = 2

    def get_address(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        registers["PC"].inc()

        address += registers["X"].get()
        # wrap on values > 0xFF
        address = address % 0xFF

        return address

    def get_value(self, flags, registers, memory):
        address = self.get_address(flags, registers, memory)

        return memory.read(address)

    def get_inst_str(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        self.get_value(flags, registers, memory)
        return "${0:02x},X".format(address)


@dataclass
class ZeroPageYAddressingMode(AddressingMode):
    """
    Zero Page Y addressing mode
    Compute the address by adding the value the PC points to
    plus the Y register value.
    Wraps if the value is greater than 0x255.
    """

    bytes: ClassVar[int] = 2

    def get_value(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        registers["PC"].inc()

        address += registers["Y"].get()
        # wrap on values > 0xFF
        address = address % 0xFF

        return memory.read(address)

    def get_inst_str(self, flags, registers, memory):
        address = memory.read(registers["PC"].get())
        self.get_value(flags, registers, memory)
        return "${0:02x},Y".format(address)


@dataclass
class RelativeAddressingMode(AddressingMode):
    """
    Relative addressing mode
    The value in the next byte is added to the PC to find the effective
    address.

    The effective address is calculated from the PC after it has been
    incremented reading the offset, not from the JMP opcode position.

    This uses two's complement, and supports negative offsets.
    """

    bytes: ClassVar[int] = 2

    def get_value(self, flags, registers, memory):
        offset = memory.read(registers["PC"].get())
        if offset > 0x7F:
            # Calculate two's complement to get negative value
            offset = -((0xFF - offset) + 1)
        # TODO: update flags

        registers["PC"].inc()

        effective_address = registers["PC"].get() + offset

        # TODO: Verify that this is correct
        return (None, effective_address % 0xFFFF)

    def get_inst_str(self, flags, registers, memory):
        "Return the address as an effective address"
        (tmp, address) = self.get_value(flags, registers, memory)
        if address is not None:
            return "${0:04x}".format(address)
        else:
            return ""
