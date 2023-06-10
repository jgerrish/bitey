from dataclasses import dataclass
import logging

from bitey.cpu.cpu import CPU, CPUState, CPUStateChange
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
        self.logger = logging.getLogger("bitey.computer.computer.Computer")
        self.cpu.reset(self.memory)

    def build_from_json(json_data):
        """
        Build a computer from a JSON representation
        """
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

    def step(self, instruction_loaded=False):
        """
        Run a single instruction

        This changes the CPU state to running, if it is not already
        running.
        """
        try:
            self.cpu.set_state(CPUState.RUNNING)
        except CPUStateChange:
            pass

        self.cpu.step(self.memory, 1, instruction_loaded)

    def reset(self):
        "Reset the computer"
        self.memory.reset()
        self.cpu.reset(self.memory)

    def set_instructions_loaded_limit(self, limit):
        """
        Set an instruction load limit on the CPU.

        Set an instruction limit on the total number of instructions
        that can be loaded.  Once that limit is reached, an action
        can be taken such as stopping the CPU.

        This limit can be changed, but calling methods such as run()
        doesn't reset the number of instructions executed.  The computer
        needs to be reset to change that.
        """
        self.cpu.num_instructions_loaded_limit = limit

    def set_instructions_executed_limit(self, limit):
        """
        Set an instruction execute limit on the CPU.

        Set an instruction execute limit on the total number of
        instructions that can be run.  Once that limit is reached, an
        action can be taken such as stopping the CPU.

        This limit can be changed, but calling methods such as run()
        doesn't reset the number of instructions executed.  The computer
        needs to be reset to change that.

        """
        self.cpu.num_instructions_executed_limit = limit

    def run(  # noqa: C901
        self,
        instruction_loaded=False,
        num_instructions_loaded_limit=None,
        num_instructions_executed_limit=None,
    ):
        """
        Run the processor

        This changes the CPU state to running, if it is not already
        running.
        """
        if num_instructions_executed_limit is not None:
            self.set_instructions_executed_limit(num_instructions_executed_limit)

        if num_instructions_loaded_limit is not None:
            self.set_instructions_loaded_limit(num_instructions_loaded_limit)

        try:
            self.cpu.set_state(CPUState.RUNNING)
        except CPUStateChange:
            pass

        # After setup() is run, the CPU is initialized into a state
        # where the first instruction is already loaded.
        if instruction_loaded:
            try:
                self.cpu.execute_instruction(self.memory)
            except CPUStateChange:
                if self.cpu.state != CPUState.RUNNING:
                    self.logger.debug(
                        "Number of instructions executed: {}".format(
                            self.cpu.num_instructions_executed
                        )
                    )
                    return

        while self.cpu.state == CPUState.RUNNING:
            try:
                self.step()
            except CPUStateChange:
                continue

        self.logger.debug(
            "Number of instructions executed: {}".format(
                self.cpu.num_instructions_executed
            )
        )

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

        If an invalid opcode is found, it prints it as "INV"
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

    def set_input_handler(self, handler):
        """
        Add a custom input handler to the computer

        Adding a custom input handler lets us use a simple computer
        from different types of IO devices including terminal or
        consoles, GUIs and other devices.  For basic usage, you can
        use the Python input() function:

        computer.set_input_handler(input("> "))
        """
        self.input_handler = handler
