import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.adc import ADC


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_adc_binary_add(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x01)
    computer.cpu.flags["D"].clear()

    # The value
    computer.memory.write(0x00, 0x02)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x03)],
        [("C", False), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_binary_add_with_previous_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x00)
    computer.cpu.flags["C"].set()

    # The value
    computer.memory.write(0x00, 0x00)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x01)],
        [("C", False), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_binary_add_carry_and_negative_flag_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0xC0)
    computer.cpu.flags["D"].clear()

    # The value
    computer.memory.write(0x00, 0xC0)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x80)],
        [("C", True), ("Z", False), ("V", False), ("N", True)],
        [],
    )


def test_cpu_instruction_adc_binary_add_negative_flag_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x80)
    computer.cpu.flags["D"].clear()

    # The value
    computer.memory.write(0x00, 0x01)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x81)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
        [],
    )


def test_cpu_instruction_adc_binary_add_carry_and_overflow_flags_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x81)
    computer.cpu.flags["D"].clear()

    # The value
    computer.memory.write(0x00, 0x80)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x01)],
        [("C", True), ("Z", False), ("V", True), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_binary_add_carry_and_zero_flags_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x80)
    computer.cpu.flags["D"].clear()

    # The value
    computer.memory.write(0x00, 0x80)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x00)],
        [("C", True), ("Z", True), ("V", True), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_decimal_add_carry_low_nibble_eights(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(8)
    # Set decimal mode
    computer.cpu.flags["D"].set()

    # The value
    computer.memory.write(0x00, 8)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0b00010110)],
        [("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_decimal_add_carry_low_nibble_nines(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(9)
    # Set decimal mode
    computer.cpu.flags["D"].set()

    # The value
    computer.memory.write(0x00, 9)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0b00011000)],
        [("C", False), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_adc_decimal_add_carry_high_nibble(setup):
    "Add carry high nibble, default NMOS chipset"
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    # decimal 50
    computer.cpu.registers["A"].set(0b01010000)
    # Set decimal mode
    computer.cpu.flags["D"].set()

    # The value
    # decimal 50
    computer.memory.write(0x00, 0b01010000)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0b00000000)],
        [("C", True), ("Z", False), ("V", True), ("N", True)],
        [],
    )


# # Some more tests


# # Test symmetry of the V flag


def test_cpu_instruction_adc_binary_add_7F_and_01(setup):
    "Add 7F and 01, expect overflow flag set, default NMOS chipset"
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x7F)
    # Set decimal mode
    computer.cpu.flags["D"].clear()

    computer.memory.write(0x00, 0x01)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x80)],
        [("C", False), ("Z", False), ("V", True), ("N", True)],
        [],
    )


def test_cpu_instruction_adc_binary_add_01_and_7F(setup):
    "Add 01 and 7F, expect overflow flag set, default NMOS chipset"
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x01)
    # Set decimal mode
    computer.cpu.flags["D"].clear()

    computer.memory.write(0x00, 0x7F)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x80)],
        [("C", False), ("Z", False), ("V", True), ("N", True)],
        [],
    )


# Test both operands greater than or equal 0x80, result less than 0x80


def test_cpu_instruction_adc_binary_add_80_and_80(setup):
    "Add 7F and 01, expect overflow flag set, default NMOS chipset"
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x80)
    # Set decimal mode
    computer.cpu.flags["D"].clear()

    computer.memory.write(0x00, 0x80)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    i1 = ADC("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", 0x00)],
        [("C", True), ("Z", True), ("V", True), ("N", False)],
        [],
    )
