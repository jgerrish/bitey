import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.sbc import SBC


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_sbc_binary_subtract(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x03)
    # inverted carry flag
    computer.cpu.flags["C"].set()

    # The value
    computer.memory.write(0x00, 0x02)

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    i1 = SBC("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x01)],
        [("C", True), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_sbc_binary_subtract_negative_result(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x01)
    computer.cpu.flags["C"].set()

    # The value
    computer.memory.write(0x00, 0x02)

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    i1 = SBC("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0xFF)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
        [],
    )

    # assert i1.result == 255
    assert i1.result == -1


def test_cpu_instruction_sbc_binary_subtract_with_borrow(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x04)
    computer.cpu.flags["D"].clear()
    computer.cpu.flags["C"].clear()

    # The value
    computer.memory.write(0x00, 0x02)

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    i1 = SBC("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x01)],
        [("C", True), ("Z", False), ("V", False), ("N", False)],
        [],
    )

    # assert i1.result == 0x101
    assert i1.result == 0x01


def test_cpu_instruction_sbc_decimal_subtract(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    # decimal 44
    computer.cpu.registers["A"].set(0b01000100)
    computer.cpu.flags["D"].set()
    computer.cpu.flags["C"].set()

    # The value, decimal 29
    computer.memory.write(0x00, 0b00101001)

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    i1 = SBC("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0b00010101)],
        [("C", True), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_sbc_decimal_subtract_with_previous_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    # decimal 29
    computer.cpu.registers["A"].set(0b00101001)
    computer.cpu.flags["D"].set()
    computer.cpu.flags["C"].set()

    # The value, decimal 44
    computer.memory.write(0x00, 0b01000100)

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    i1 = SBC("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x85)],  # 0b00010101)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
        [],
    )
