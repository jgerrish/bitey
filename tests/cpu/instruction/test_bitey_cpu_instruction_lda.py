import pytest

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImmediateAddressingMode,
    ZeroPageAddressingMode,
)
import tests.computer.computer

from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ld import LDA


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    computer.reset()
    computer.cpu.registers["PC"].set(0x01)
    yield computer


def init_memory(memory, init_list):
    """
    Setup memory for tests
    The first argument is the Memory
    The second argument is a list of 2-tuples
    Each 2-tuple contains an address what value should be stored there
    """
    for item in init_list:
        memory.write(item[0], item[1])


def execute_instruction(
    computer, opcode, expected_a_register, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = LDA("LDA", opcode, "Load Accumulator with Memory")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"] == expected_a_register
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_lda_immediate(setup):
    "Test LDA in immediate addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0x2B)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x2B, False, False)


def test_cpu_instruction_lda_immediate_zero(setup):
    "Test LDA in immediate addressing mode that loads a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0x00)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True, False)


def test_cpu_instruction_lda_immediate_nonnegative(setup):
    "Test LDA in immediate addressing mode that doesn't load a negative number"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0b01111111)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01111111, False, False)


def test_cpu_instruction_lda_immediate_zero_negative(setup):
    "Test LDA in immediate addressing mode that loads a negative number"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0b10000000)])

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10000000, False, True)


def test_cpu_instruction_lda_zeropage(setup):
    "Test LDA in zero page addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x55)])

    i1_opcode = Opcode(165, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x55, False, False)


def test_cpu_instruction_lda_zeropage_zero(setup):
    "Test LDA in zero page addressing mode that loads a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x00)])

    i1_opcode = Opcode(169, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True, False)


def test_cpu_instruction_lda_absolute(setup):
    "Test LDA in absolute addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x20)])

    i1_opcode = Opcode(173, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x20, False, False)


def test_cpu_instruction_lda_absolute_zero(setup):
    "Test LDA in absolute addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x00)])

    i1_opcode = Opcode(173, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True, False)
