import pytest
import tests.computer.computer
from tests.computer.computer import run_adc_test


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


# Test Overflow Flag differences


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_78_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x78,
        False,
        0x78,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_78_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x78,
        True,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_79_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x79,
        False,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_79_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x79,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_7A_carry_0_overflow(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x7A,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_7A_carry_1_overflow(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x7A,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Test symmetric 0x7A + 0x00 adds


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_7A_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x7A,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_7A_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x7A,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Test Carry Flag differences


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_98_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x98,
        False,
        0x98,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_98_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x98,
        True,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_99_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x99,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_00_plus_99_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x00,
        0x99,
        True,
        0x00,
        # [("C", True), ("Z", False), ("V", True)],#, ("N", True)],
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


# Carry and overflow difference test


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_40_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x40,
        False,
        0x78,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_40_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x40,
        True,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_41_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x41,
        False,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_41_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x41,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_42_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x42,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_38_plus_42_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x38,
        0x42,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Other tests


def test_cpu_instruction_adc_decimal_add_nmos_50_plus_50_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x50,
        0x50,
        False,
        0x00,
        [("C", True), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_50_plus_50_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x50,
        0x50,
        True,
        0x01,
        [("C", True), ("Z", False), ("V", True)],
    )


# These test regions around

# [(110, 14), (94, 30), (78, 46), (62, 62), (46, 78), (30, 94), (14, 110)]
# and
# [(237, 140), (221, 156), (205, 172), (189, 188), (173, 204), (157, 220), (141, 236)]


def test_cpu_instruction_adc_decimal_add_nmos_3E_plus_3E_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x3E,
        0x3E,
        False,
        0x72,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_3E_plus_3E_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x3E,
        0x3E,
        True,
        0x73,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_BB_plus_C0_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0xBB,
        0xC0,
        False,
        0xE1,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_BB_plus_C0_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0xBB,
        0xC0,
        True,
        0xE2,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_3A_plus_42_carry_0(setup):
    run_adc_test(
        "nmos",
        True,
        0x3A,
        0x42,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_decimal_add_nmos_3A_plus_42_carry_1(setup):
    run_adc_test(
        "nmos",
        True,
        0x3A,
        0x42,
        True,
        0x83,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )
