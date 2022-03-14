from dataclasses import dataclass


@dataclass
class Flag:
    """
    Processor flag or status register
    Examples can include the carry flag and overflow flag
    """

    short_name: str
    """
    The short name of the flag
    Usually this is a single character such as C for the carry flag
    """

    name: str
    """
    The name of the flag
    For example, Carry for the carry flag
    """

    bit_field_pos: int
    "If the flag is stored in a bitfield, which bit position is it"

    status: bool
    "Store the state of the register in a boolean flag"

    # flags: Flags
    # "Reference to the Flags object that owns this flag"

    def __post_init__(self):
        self.flags = None

    def set(self):
        "Set this flag.  Set it to true."
        self.status = True
        if self.flags is not None:
            self.flags.set_bit(self.short_name)

    def clear(self):
        "Clear this flag.  Set it to False."
        self.status = False
        if self.flags is not None:
            self.flags.clear_bit(self.short_name)


@dataclass
class Flags:
    """
    Define a set of processor flags
    """

    flags: list[Flag]
    data: int

    def __post_init__(self):
        "Create a dictionary so we can access flags by short name"
        self.flag_dict = {}
        for f in self.flags:
            self.flag_dict[f.short_name] = f

        # Create a reference in each Flag to this Flags object
        for f in self.flags:
            f.flags = self

        self.data = 0

    def __getitem__(self, i):
        return self.flag_dict[i]

    def set(self, flag):
        "Set a flag and the bit in the flags byte"
        self[flag].set()
        self.set_bit(flag)

    def set_bit(self, flag):
        """
        Set a flag bit in the flags byte
        This is a private method
        """
        bit = 2 ** self[flag].bit_field_pos
        self.data = self.data | bit

    def clear(self, flag):
        "Clear a flag and the bit in the flags byte"
        self[flag].clear()
        self.clear_bit(flag)

    def clear_bit(self, flag):
        """
        Clear a flag bit in the flags byte
        This is a private method
        """
        # Clear the bit
        bit = 2 ** self[flag].bit_field_pos
        self.data = self.data & (0xFF - bit)
