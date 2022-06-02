import pytest
import tests.computer.computer
from tests.computer.computer import run_sbc_test
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_00_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0x00,
        False,
        0x99,
        # [("C", False)],#, ("Z", False), ("V", False), ("N", True)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_00_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0x00,
        True,
        0x00,
        [],
        # [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_01_minus_01_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x01,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_01_minus_01_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x01,
        True,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
        # [("C", False), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_02_minus_01_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x02,
        0x01,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_02_minus_01_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x02,
        0x01,
        True,
        0x01,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_01_minus_02_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x02,
        False,
        0x98,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_01_minus_02_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x02,
        True,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_99_minus_00_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x99,
        0x00,
        False,
        0x98,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_99_minus_00_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x99,
        0x00,
        True,
        0x99,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_AA_minus_00_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0xAA,
        0x00,
        False,
        0xA9,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_AA_minus_00_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0xAA,
        0x00,
        True,
        0xAA,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_AA_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0xAA,
        False,
        0xEF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_AA_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0xAA,
        True,
        0xF0,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_44_minus_22_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x44,
        0x22,
        False,
        0x21,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_44_minus_22_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x44,
        0x22,
        True,
        0x22,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_22_minus_13_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x22,
        0x13,
        False,
        0x08,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_22_minus_13_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x22,
        0x13,
        True,
        0x09,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_04_minus_13_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x04,
        0x13,
        False,
        0x90,
        # [("C", False), ("Z", False), ("V", False), ("N", True)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_04_minus_13_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x04,
        0x13,
        True,
        0x91,
        # [("C", False), ("Z", False), ("V", False), ("N", True)],
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_11_minus_23_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x11,
        0x23,
        False,
        0x87,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_11_minus_23_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x11,
        0x23,
        True,
        0x88,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_0B_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0x0B,
        False,
        0x8E,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_cmos_00_minus_0B_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x00,
        0x0B,
        True,
        0x8F,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_0(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x80,
        False,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_1(setup):
    run_sbc_test(
        "cmos",
        True,
        0x01,
        0x80,
        True,
        0x21,
        [("C", False), ("Z", False), ("V", True), ("N", False)],
    )
