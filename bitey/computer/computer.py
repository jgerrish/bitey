from dataclasses import dataclass
import logging

from bitey.logger import setup_logger
from bitey.cpu.cpu import CPU
from bitey.memory.memory import Memory


@dataclass
class Computer:
    """
    Base class for a computer
    """

    cpu: CPU
    "The CPU for the computer"

    memory: Memory
    "The memory for the processor"

    def __post_init__(self):
        """
        Called after the generated __init__ method
        Initialize the computer
        """
        setup_logger()
        self.logger = logging.getLogger("bitey")
        self.cpu.reset(self.memory)

    def build_from_json(json_data):
        setup_logger()
        logger = logging.getLogger("bitey")
        logger.debug("Building computer")
        cpu = CPU.build_from_json(json_data)
        logger.debug("Allocating memory")
        memory = Memory(bytearray(65536))

        return Computer(cpu, memory)

    def load(self, data, offset=0):
        """
        Load data into memory
        Loads data into memory at offset
        """
        for byte in data:
            if offset < len(self.memory):
                self.memory.write(offset, byte)
                offset += 1
            else:
                break

    def run(self):
        self.cpu.execute_instruction()
