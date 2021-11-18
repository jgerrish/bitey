from dataclasses import dataclass

class MemoryOutOfRange(Exception):
    "Attempt to access memory beyond the size of the memory"

@dataclass
class Memory:
    """
    Random Access Memory
    """

    "The memory"
    memory: bytearray()

    def __init__(self, size=0):
        "Initialize the memory to size bytes"
        self.memory = bytearray(size)

    def __len__(self):
        "Get the size of the memory"
        return len(self.memory)

    def read(self, address):
        """
        Read a byte from memory
        address is the location in memory to read from
        """
        if (address >= 0) and (address < len(self.memory)):
            return self.memory[address]
        else:
            raise MemoryOutOfRange

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
        adl = self.memory[adl_address]
        adh = self.memory[adh_address]

        return self.get_16bit_address(adl, adh)
