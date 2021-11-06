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
    adl: int

    "The high-order byte"
    adh: int
