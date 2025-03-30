import pytest

import tests.computer.computer

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ora import ORA


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


def execute_instruction(
    computer, opcode, expected_a_register, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = ORA("ORA", opcode, "OR Memory with Accumulator")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].get() == expected_a_register
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_ora_immediate(setup):
    "Test ORA in immediate addressing mode that doesn't load a zero"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b101100)
    init_memory(computer.memory, [(1, 0b101011)])

    i1_opcode = Opcode(0x09, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0b101111, False, False)


def test_cpu_instruction_ora_immediate_zero(setup):
    "Test ORA in immediate addressing mode that loads a zero"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0x00)
    init_memory(computer.memory, [(1, 0x00)])

    i1_opcode = Opcode(0x09, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True, False)


def test_cpu_instruction_ora_immediate_nonnegative(setup):
    "Test ORA in immediate addressing mode that doesn't load a negative number"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b01111111)
    init_memory(computer.memory, [(1, 0b00000001)])

    i1_opcode = Opcode(0x09, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01111111, False, False)


def test_cpu_instruction_ora_immediate_zero_negative(setup):
    "Test ORA in immediate addressing mode that loads a negative number"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b10000000)
    init_memory(computer.memory, [(1, 0b10000001)])

    i1_opcode = Opcode(0x09, ImmediateAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10000001, False, True)
