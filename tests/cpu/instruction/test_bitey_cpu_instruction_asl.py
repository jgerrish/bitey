import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import AccumulatorAddressingMode, ZeroPageAddressingMode
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.asl import ASL


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(
    computer,
    opcode,
    expected_a_register,
    expected_c_flag,
    expected_z_flag,
    expected_n_flag,
):
    """
    Execute the instruction based on an opcode
    TODO: refactor this to work with expected memory or registers.
    """
    flags = computer.cpu.flags
    i1 = ASL("ASL", opcode, "Shift Left One Bit (Memory or Accumulator)")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].get() == expected_a_register
        assert flags["C"].status is expected_c_flag
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_asl_accumulator_addressing_mode_no_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b00101011)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01010110, False, False, False)


def test_cpu_instruction_asl_accumulator_addressing_mode_carry_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b10101011)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01010110, True, False, False)


def test_cpu_instruction_asl_accumulator_addressing_mode_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b00000000)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b00000000, False, True, False)


def test_cpu_instruction_asl_accumulator_addressing_mode_carry_and_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b10000000)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b00000000, True, True, False)


def test_cpu_instruction_asl_accumulator_addressing_mode_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b01000000)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10000000, False, False, True)


def test_cpu_instruction_asl_accumulator_addressing_mode_carry_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b11000000)

    i1_opcode = Opcode(0x0A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10000000, True, False, True)


def test_cpu_instruction_asl_zeropage_addressing_mode_no_carry(setup):
    computer = setup
    computer.reset()

    a = computer.cpu.registers["A"].get()
    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b00101011)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, False, False, False)
    assert computer.memory.read(0xA6) == 0b01010110


def test_cpu_instruction_asl_zeropage_addressing_mode_carry_flag(setup):
    computer = setup
    computer.reset()

    a = computer.cpu.registers["A"].get()
    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b10101011)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, True, False, False)

    assert computer.memory.read(0xA6) == 0b01010110


def test_cpu_instruction_asl_zeropage_addressing_mode_zero_flag(setup):
    computer = setup
    computer.reset()

    a = computer.cpu.registers["A"].get()
    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b00000000)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, False, True, False)
    assert computer.memory.read(0xA6) == 0b00000000


def test_cpu_instruction_asl_zeropage_addressing_mode_carry_and_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    a = computer.cpu.registers["A"].get()
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b10000000)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, True, True, False)
    assert computer.memory.read(0xA6) == 0b00000000


def test_cpu_instruction_asl_zeropage_addressing_mode_negative_flag(setup):
    computer = setup
    computer.reset()

    a = computer.cpu.registers["A"].get()
    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b01000000)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, False, False, True)
    assert computer.memory.read(0xA6) == 0b10000000


def test_cpu_instruction_asl_zeropage_addressing_mode_carry_and_negative_flag(setup):
    computer = setup
    computer.reset()

    a = computer.cpu.registers["A"].get()
    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b11000000)

    i1_opcode = Opcode(0x06, ZeroPageAddressingMode())
    execute_instruction(computer, i1_opcode, a, True, False, True)
    assert computer.memory.read(0xA6) == 0b10000000
