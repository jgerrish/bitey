from dataclasses import dataclass
import logging

from bitey.logger import setup_logger
from bitey.cpu.cpu import CPU
from bitey.cpu.instruction.instruction import UndocumentedInstruction
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
        self.logger = logging.getLogger("bitey.computer.computer.Computer")
        self.cpu.reset(self.memory)

    def build_from_json(json_data):
        """
        Build a computer from a JSON representation
        """
        setup_logger()
        logger = logging.getLogger("bitey.computer.computer.Computer")
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
        "Run a single instruction"
        self.cpu.execute_instruction()

    def reset(self):
        "Reset the computer"
        self.cpu.reset(self.memory)

    def parse(self):
        """
        Parse the next instruction.
        Returns a tuple with the decoded instruction along with the bytes
        consumed.

        This is a destructive operation since it changes the Program
        Counter.
        """
        consumed = 0
        instruction = None

        try:
            instruction = self.cpu.get_next_instruction(self.memory)
            addressing_mode = instruction.opcode.addressing_mode
            consumed = addressing_mode.bytes
        except UndocumentedInstruction:
            self.logger.debug(
                "Found undocumented instruction at address 0x{0:02x}".format(
                    self.cpu.registers["PC"].value - 1
                )
            )
            consumed = 1

        return (instruction, consumed)

    def disassemble(self):
        """
        Disassemble the Memory associated with this Computer instance
        See the disassembler example in the examples directory for
        how to use this.

        Return a string of the disassembly.

        This is a destructive operation, since it changes the
        Program Counter.

        It might make more sense to include this as a method on
        Memory, but it uses and tests the existing execution machinery.
        """
        total_consumed = 0
        self.cpu.registers["PC"].set(0x00)
        lines = []

        while total_consumed < len(self.memory):
            result = ""
            (instruction, consumed) = self.parse()
            data = self.memory.read_range(total_consumed, total_consumed + consumed)
            inst_bytes = " ".join(["{:02x}".format(x) for x in data])
            result += "{:04x}  {:<8}  ".format(total_consumed, inst_bytes)
            if instruction is not None:
                result += instruction.assembly_str(self)
            else:
                result += "{}".format("INV")
            lines.append(result)
            total_consumed += consumed

        return "\n".join(lines)
