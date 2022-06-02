import pytest
import tests.computer.computer
from tests.computer.computer import run_sbc_test


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x00,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_00_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x00,
        True,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_01_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x01,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_01_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x01,
        True,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_02_minus_01_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x02,
        0x01,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_02_minus_01_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x02,
        0x01,
        True,
        0x01,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_02_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x02,
        False,
        0x98,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_02_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x02,
        True,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_99_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x99,
        0x00,
        False,
        0x98,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_99_minus_00_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x99,
        0x00,
        True,
        0x99,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_AA_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0xAA,
        0x00,
        False,
        0xA9,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_AA_minus_00_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0xAA,
        0x00,
        True,
        0xAA,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_AA_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0xAA,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_AA_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0xAA,
        True,
        0xF0,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_44_minus_22_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x44,
        0x22,
        False,
        0x21,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_44_minus_22_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x44,
        0x22,
        True,
        0x22,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_22_minus_13_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x22,
        0x13,
        False,
        0x08,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_22_minus_13_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x22,
        0x13,
        True,
        0x09,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_04_minus_13_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x04,
        0x13,
        False,
        0x90,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_04_minus_13_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x04,
        0x13,
        True,
        0x91,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_11_minus_23_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x11,
        0x23,
        False,
        0x87,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_11_minus_23_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x11,
        0x23,
        True,
        0x88,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_0B_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x0B,
        False,
        0x9E,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_0B_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x0B,
        True,
        0x9F,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_20_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x20,
        False,
        0x79,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_20_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x20,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


# Some additional tests around change-points


def test_cpu_instruction_sbc_decimal_subtract_nmos_80_minus_13_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x80,
        0x13,
        False,
        0x66,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_80_minus_13_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x80,
        0x13,
        True,
        0x67,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_7F_minus_FE_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x7F,
        0xFE,
        False,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_7F_minus_FE_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x7F,
        0xFE,
        True,
        0x21,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_7E_minus_FE_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x7E,
        0xFE,
        False,
        0x19,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_7E_minus_FE_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x7E,
        0xFE,
        True,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x80,
        False,
        0x19,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x80,
        False,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x81,
        False,
        0x19,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_FF_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0xFF,
        0x7F,
        False,
        0x79,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_80_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0x80,
        True,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x80,
        True,
        0x21,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_81_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x81,
        True,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_FF_minus_7F_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0xFF,
        0x7F,
        True,
        0x80,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )
