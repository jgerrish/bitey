import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import AbsoluteAddressingMode, ZeroPageAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.bit import BIT


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_bit_zeropage(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x21)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x3C)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", False), ("N", False)], []
    )

    assert i1.result == 0x20


def test_cpu_instruction_bit_zeropage_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x61)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x9D)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", False), ("N", True)], []
    )

    assert i1.result == 0x01


def test_cpu_instruction_bit_zeropage_overflow_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9D)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x61)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", True), ("N", False)], []
    )

    assert i1.result == 0x01


def test_cpu_instruction_bit_zeropage_overflow_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9D)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0xE1)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", True), ("N", True)], []
    )

    assert i1.result == 0x81


def test_cpu_instruction_bit_zeropage_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x1C)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x21)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", False), ("N", False)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_zeropage_zero_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x61)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x9C)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", False), ("N", True)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_zeropage_zero_and_overflow_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9C)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0x61)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", True), ("N", False)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_zeropage_zero_and_overflow_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x1C)
    # The zero page location to read the value from
    computer.memory.write(0x00, 0x01)
    # The value
    computer.memory.write(0x01, 0xE1)

    i1_opcode = Opcode(0x24, ZeroPageAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", True), ("N", True)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_absolute(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x21)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)
    # The value
    computer.memory.write(0x02, 0x3C)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", False), ("N", False)], []
    )

    assert i1.result == 0x20


def test_cpu_instruction_bit_absolute_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x61)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0x9D)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", False), ("N", True)], []
    )

    assert i1.result == 0x01


def test_cpu_instruction_bit_absolute_overflow_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9D)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0x61)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", True), ("N", False)], []
    )

    assert i1.result == 0x01


def test_cpu_instruction_bit_absolute_overflow_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9D)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0xE1)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", False), ("V", True), ("N", True)], []
    )

    assert i1.result == 0x81


def test_cpu_instruction_bit_absolute_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x1C)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0x21)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", False), ("N", False)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_absolute_zero_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x61)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0x9C)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", False), ("N", True)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_absolute_zero_and_overflow_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x9C)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0x61)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", True), ("N", False)], []
    )

    assert i1.result == 0x00


def test_cpu_instruction_bit_absolute_zero_and_overflow_and_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.registers["A"].set(0x1C)
    # The memory location to read the value from
    computer.memory.write(0x00, 0x02)
    computer.memory.write(0x01, 0x00)

    # The value
    computer.memory.write(0x02, 0xE1)

    i1_opcode = Opcode(0x2C, AbsoluteAddressingMode())
    i1 = BIT("BIT", i1_opcode, "Test Bits in Memory with Accumulator")

    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("Z", True), ("V", True), ("N", True)], []
    )

    assert i1.result == 0x00
