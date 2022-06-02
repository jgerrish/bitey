import pytest
from tests.computer.computer import run_adc_test
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


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
