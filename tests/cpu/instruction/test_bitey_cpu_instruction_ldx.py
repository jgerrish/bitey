import pytest

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImmediateAddressingMode,
    ZeroPageAddressingMode,
)
import tests.computer.computer

from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ld import LDX


def init_memory(memory, init_list):
    """
    Setup memory for tests
    The first argument is the Memory
    The second argument is a list of 2-tuples
    Each 2-tuple contains an address what value should be stored there
    """
    for item in init_list:
        memory.write(item[0], item[1])


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(computer, opcode, expected_a_register, expected_z_flag):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = LDX("LDX", opcode, "Load Accumulator with Memory")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["X"] == expected_a_register
        assert flags["Z"].status is expected_z_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_ldx_immediate(setup):
    "Test LDX in immediate addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0x2B)])

    i1_opcode = Opcode(0xA2, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x2B, False)


def test_cpu_instruction_ldx_immediate_zero(setup):
    "Test LDX in immediate addressing mode that loads a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(1, 0x00)])

    i1_opcode = Opcode(0xA2, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)


def test_cpu_instruction_ldx_zeropage(setup):
    "Test LDX in zero page addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x55)])

    i1_opcode = Opcode(0xA6, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x55, False)


def test_cpu_instruction_ldx_zeropage_zero(setup):
    "Test LDX in zero page addressing mode that loads a zero"
    computer = setup
    computer.reset()

    init_memory(computer.memory, [(0x01, 0x2B), (0x2B, 0x00)])

    i1_opcode = Opcode(0xA6, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)


def test_cpu_instruction_ldx_absolute(setup):
    "Test LDX in absolute addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x20)])

    i1_opcode = Opcode(0xAE, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x20, False)


def test_cpu_instruction_ldx_absolute_zero(setup):
    "Test LDX in absolute addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    # Address low, address high and value to load
    init_memory(computer.memory, [(0x01, 0x60), (0x02, 0xEE), (0xEE60, 0x00)])

    i1_opcode = Opcode(0xAE, AbsoluteAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True)
