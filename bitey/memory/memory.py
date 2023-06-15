from dataclasses import dataclass


class MemoryOutOfRange(Exception):
    "Attempt to access memory beyond the size of the memory"


@dataclass
class Memory:
    """
    Random Access Memory

    The standard layout for the 6500 series is:
    0x0000 - 0x00FF Zero Page and indirect addressing space
    0x0100 - 0x01FF Stack and absolute addressing space
    0x0200 - 0x3FFF RAM
    0x4000 - 0x7FFF I/O
    0x8000 - 0xFFF9 Program Storage / ROM
    0xFFFA          Vector low address for NMI
    0xFFFB          Vector high address for NMI
    0xFFFC          Vector low address for RESET
    0xFFFD          Vector high address for RESET
    0xFFFE          Vector low address for IRQ + BRK
    0xFFFF          Vector high address for IRQ + BRK
    """

    memory: bytearray()
    "The memory"

    def __init__(self, size=0):
        "Initialize the memory to size bytes"
        self.size = size
        self.memory = bytearray(size)

    def __len__(self):
        "Get the size of the memory"
        return len(self.memory)

    def reset(self):
        "Reset the memory to zero"
        self.memory = bytearray(self.size)

    def read(self, address):
        """
        Read a byte from memory
        address is the location in memory to read from
        """
        if (address >= 0) and (address < len(self.memory)):
            return self.memory[address]
        else:
            raise MemoryOutOfRange

    def read_range(self, start, end):
        """
        Return a range of bytes.
        The start and end match Python slice meaning.
        The range includes the start location but not the end location.
        e.g. start=0, end=1 returns one byte in read_range.
        Raise an exception if the memory access is out of range.
        """
        if (start < 0) or (end > len(self.memory)):
            raise MemoryOutOfRange
        else:
            return self.memory[start:end]

    def write(self, address, value):
        """
        Write a value in memory
        address is the location to write to
        value is the value to write
        """
        if (address >= 0) and (address < len(self.memory)):
            self.memory[address] = value
        else:
            raise MemoryOutOfRange

    def get_16bit_address(self, adl, adh):
        """
        Compute a 16-bit address from a low and high byte.
        adl is the low byte
        adh is the high byte
        """
        return adl + (adh << 8)

    def get_16bit_value(self, adl_address, adh_address):
        """
        Get a 16bit value from memory.
        Compute a 16-bit value from two consecutive bytes in memory.
        This can be used to build a 16-bit address for example.
        """
        adl = self.read(adl_address)
        adh = self.read(adh_address)

        return self.get_16bit_address(adl, adh)

    def memory_dump(self, address=None):
        """
        Dump a range of memory starting at an address

        Defaults to the zero page.
        Rounds down the range to a 16-byte boundary.

        Example:

        from bitey.memory.memory import Memory
        b = bytes(range(256)) * 10
        m = Memory(b)
        print(m.memory_dump(32))
        """

        if address is None:
            address = 0
        end = 0
        end = min(address + 32, len(self.memory))
        return self.memory_range_dump(range(address, end))

    def memory_range_dump(self, memory_range=None):
        """
        Dump a range of memory

        Defaults to the zero page.
        Rounds down the range to a 16-byte boundary.

        Example:

        from bitey.memory.memory import Memory
        b = bytes(range(256)) * 10
        m = Memory(b)
        print(m.memory_range_dump(range(32, 64)))
        """
        memory_dump = []
        memory_range_len = None
        num_lines = 0
        if memory_range is None:
            memory_range = range(0x00, 0x100)

        if (memory_range.start < 0) or (memory_range.stop > len(self.memory)):
            raise MemoryOutOfRange

        memory_range_len = len(memory_range)
        num_lines = memory_range_len // 16
        for line_index in range(num_lines):
            line = []
            line.append("0x{:04x} ".format(line_index * 0x10 + memory_range.start))
            for x in range(
                line_index * 0x10 + memory_range.start,
                line_index * 0x10 + 0x08 + memory_range.start,
            ):
                line.append("{:02x}".format(self.memory[x]))
            line.append("")
            for x in range(
                line_index * 0x10 + 0x08 + memory_range.start,
                line_index * 0x10 + 0x10 + memory_range.start,
            ):
                line.append("{:02x}".format(self.memory[x]))
            memory_dump.append("{}".format(" ".join(line)))
        memory_dump = "\n".join(memory_dump)

        return memory_dump
