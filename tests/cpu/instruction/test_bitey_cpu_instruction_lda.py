# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImmediateAddressingMode,
    ZeroPageAddressingMode,
)
from bitey.computer.computer import Computer
from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.lda import LDA


def build_computer():
    "Build the computer"
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def init_computer():
    "Initialize computer for tests"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].get() == 1

    return computer


def init_memory(memory, init_list):
    """
    Setup memory for tests
    The first argument is the Memory
    The second argument is a list of 2-tuples
    Each 2-tuple contains an address what value should be stored there
    """
    for item in init_list:
        memory.write(item[0], item[1])


def execute_instruction(computer, opcode, expected_a_register, expected_z_flag):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = LDA("LDA", opcode, "Load Accumulator with Memory")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"] == expected_a_register
        assert flags["Z"].status is expected_z_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_lda_immediate():
    "Test LDA in immediate addressing mode that doesn't load a zero"
    computer = init_computer()

    init_memory(computer.memory, [(1, 0x2B)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x2B, False)


def test_cpu_instruction_lda_immediate_zero():
    "Test LDA in immediate addressing mode that loads a zero"
    computer = init_computer()

    init_memory(computer.memory, [(1, 0x00)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)


def test_cpu_instruction_lda_zeropage():
    "Test LDA in zero page addressing mode that doesn't load a zero"
    computer = init_computer()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x55)])

    i1_opcode = Opcode(165, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x55, False)


def test_cpu_instruction_lda_zeropage_zero():
    "Test LDA in zero page addressing mode that loads a zero"
    computer = init_computer()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x00)])

    i1_opcode = Opcode(169, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)


def test_cpu_instruction_lda_absolute():
    "Test LDA in absolute addressing mode that doesn't load a zero"
    computer = init_computer()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x20)])

    i1_opcode = Opcode(173, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x20, False)


def test_cpu_instruction_lda_absolute_zero():
    "Test LDA in absolute addressing mode that doesn't load a zero"
    computer = init_computer()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x00)])

    i1_opcode = Opcode(173, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)
