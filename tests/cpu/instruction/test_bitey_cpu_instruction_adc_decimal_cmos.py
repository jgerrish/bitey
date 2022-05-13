import pytest
import re

import tests.computer.computer
import tests.memory.memory

from bitey.computer.computer import Computer
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.adc import ADCCMOS, ADCNMOS


def build_computer(chip_line=None):
    computer = None

    search = re.compile(".*[^a-zA-Z0-9_-].*")

    if (chip_line is not None) and (search.search(chip_line) is not None):
        raise Exception("Invalid chip_line, contains non-alphanumeric characters")

    fn = "chip/6502.json"
    if chip_line is not None:
        fn = "chip/{}-6502.json".format(chip_line)
    with open(fn) as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def run_adc_test(
    chip,
    decimal_mode,
    accumulator,
    memory,
    carry,
    expected_accumulator,
    expected_flags,
):
    if (chip == "nmos") or (chip == "cmos"):
        computer = build_computer(chip)
    else:
        computer = build_computer()

    computer.reset()
    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(accumulator)

    if decimal_mode:
        computer.cpu.flags["D"].set()
    else:
        computer.cpu.flags["D"].clear()

    if carry:
        computer.cpu.flags["C"].set()
    else:
        computer.cpu.flags["C"].clear()

    computer.memory.write(0x00, memory)

    i1_opcode = Opcode(0x69, ImmediateAddressingMode())
    if chip == "nmos":
        i1 = ADCNMOS("ADC", i1_opcode, "Add Memory to Accumulator with Carry")
    elif chip == "cmos":
        i1 = ADCCMOS("ADC", i1_opcode, "Add Memory to Accumulator with Carry")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", expected_accumulator)],
        expected_flags,
        [],
    )


# Test Overflow Flag differences


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_78_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x78,
        False,
        0x78,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_78_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x78,
        True,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_79_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x79,
        False,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_79_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x79,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_7A_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x7A,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_7A_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x7A,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Test Carry Flag differences


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_98_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x98,
        False,
        0x98,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_98_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x98,
        True,
        0x99,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_99_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x99,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_00_plus_99_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x00,
        0x99,
        True,
        0x00,
        [("C", True), ("Z", True), ("V", True), ("N", False)],
    )


# Carry and overflow difference test


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_40_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x40,
        False,
        0x78,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_40_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x40,
        True,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_41_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x41,
        False,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_41_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x41,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_42_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x42,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_38_plus_42_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x38,
        0x42,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Other tests


def test_cpu_instruction_adc_decimal_add_cmos_50_plus_50_carry_0(setup):
    run_adc_test(
        "cmos",
        True,
        0x50,
        0x50,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_cmos_50_plus_50_carry_1(setup):
    run_adc_test(
        "cmos",
        True,
        0x50,
        0x50,
        True,
        0x01,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )
