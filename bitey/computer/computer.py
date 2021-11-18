from dataclasses import dataclass

from bitey.cpu.cpu import CPU
from bitey.memory.memory import Memory


@dataclass
class Computer:
    """
    Base class for a computer
    """

    cpu: CPU

    memory: Memory

    def __post_init__(self):
        """
        Called after the generated __init__ method
        Initialize the computer
        """
        self.cpu.reset(self.memory)

    def build_from_json(json_data):
        cpu = CPU.build_from_json(json_data)
        memory = Memory(bytearray(65536))

        return Computer(cpu, memory)

    def load(self, data, offset=0):
        """
        Load data into memory
        Loads data into memory at offset
        """
        location = offset
        for byte in data:
            if offset < len(self.memory):
                self.memory.write(offset, byte)
                offset += 1
            else:
                break

    def run(self):
        cpu.execute_instruction()
