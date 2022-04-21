import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import AccumulatorAddressingMode, ZeroPageAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.lsr import LSR


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(
    computer,
    opcode,
    expected_registers,
    expected_flags,
    expected_memory,
):
    """
    Execute the instruction based on an opcode
    """
    instruction = LSR("LSR", opcode, "Right Shift One Bit (Memory or Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        opcode,
        instruction,
        expected_registers,
        expected_flags,
        expected_memory,
    )


def test_cpu_instruction_lsr_accumulator_addressing_mode_no_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b01010110)

    i1_opcode = Opcode(0x4A, AccumulatorAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [("A", 0b00101011)],
        [("C", False), ("Z", False), ("N", False)],
        [],
    )


def test_cpu_instruction_lsr_accumulator_addressing_mode_carry_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b10101011)

    i1_opcode = Opcode(0x4A, AccumulatorAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [("A", 0b01010101)],
        [("C", True), ("Z", False), ("N", False)],
        [],
    )


def test_cpu_instruction_lsr_accumulator_addressing_mode_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b00000000)

    i1_opcode = Opcode(0x4A, AccumulatorAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [("A", 0b00000000)],
        [("C", False), ("Z", True), ("N", False)],
        [],
    )


def test_cpu_instruction_lsr_accumulator_addressing_mode_carry_and_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b00000001)

    i1_opcode = Opcode(0x4A, AccumulatorAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [("A", 0b00000000)],
        [("C", True), ("Z", True), ("N", False)],
        [],
    )


def test_cpu_instruction_lsr_zeropage_addressing_mode_no_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b00101010)

    i1_opcode = Opcode(0x46, ZeroPageAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [],
        [("C", False), ("Z", False), ("N", False)],
        [(0xA6, 0b00010101)],
    )


def test_cpu_instruction_lsr_zeropage_addressing_mode_carry_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b10101011)

    i1_opcode = Opcode(0x46, ZeroPageAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [],
        [("C", True), ("Z", False), ("N", False)],
        [(0xA6, 0b01010101)],
    )


def test_cpu_instruction_lsr_zeropage_addressing_mode_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b00000000)

    i1_opcode = Opcode(0x46, ZeroPageAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [],
        [("C", False), ("Z", True), ("N", False)],
        [(0xA6, 0b00000000)],
    )


def test_cpu_instruction_lsr_zeropage_addressing_mode_carry_and_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.memory.write(0x00, 0xA6)
    computer.memory.write(0xA6, 0b00000001)

    i1_opcode = Opcode(0x46, ZeroPageAddressingMode())
    execute_instruction(
        computer,
        i1_opcode,
        [],
        [("C", True), ("Z", True), ("N", False)],
        [(0xA6, 0b00000000)],
    )
