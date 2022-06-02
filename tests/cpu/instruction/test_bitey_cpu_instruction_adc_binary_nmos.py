import pytest
from tests.computer.computer import run_adc_test
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_adc_binary_add_nmos_00_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x00,
        False,
        0x00,
        [("C", False), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_00_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x00,
        True,
        0x01,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_01_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x01,
        False,
        0x02,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_01_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x01,
        True,
        0x03,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_02_plus_01_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x02,
        0x01,
        False,
        0x03,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_02_plus_01_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x02,
        0x01,
        True,
        0x04,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_02_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x02,
        False,
        0x03,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_02_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x02,
        True,
        0x04,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_99_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x99,
        0x00,
        False,
        0x99,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_99_plus_00_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x99,
        0x00,
        True,
        0x9A,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_AA_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xAA,
        0x00,
        False,
        0xAA,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_AA_plus_00_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0xAA,
        0x00,
        True,
        0xAB,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_AA_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0xAA,
        False,
        0xAA,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_AA_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0xAA,
        True,
        0xAB,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_44_plus_22_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x44,
        0x22,
        False,
        0x66,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_44_plus_22_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x44,
        0x22,
        True,
        0x67,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_22_plus_13_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x22,
        0x13,
        False,
        0x35,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_22_plus_13_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x22,
        0x13,
        True,
        0x36,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_04_plus_13_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x04,
        0x13,
        False,
        0x17,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_04_plus_13_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x04,
        0x13,
        True,
        0x18,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_11_plus_23_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x11,
        0x23,
        False,
        0x34,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_11_plus_23_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x11,
        0x23,
        True,
        0x35,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_0B_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x0B,
        False,
        0x0B,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_0B_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x0B,
        True,
        0x0C,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_20_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x20,
        False,
        0x20,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_20_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x20,
        True,
        0x21,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


# Some additional tests around change-points


def test_cpu_instruction_adc_binary_add_nmos_80_plus_13_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x13,
        False,
        0x93,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_13_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x13,
        True,
        0x94,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_FE_carry_0_changepoints(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0xFE,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_FE_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0xFE,
        True,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7E_plus_FE_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7E,
        0xFE,
        False,
        0x7C,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7E_plus_FE_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x7E,
        0xFE,
        True,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_adc_binary_add_nmos_00_plus_80_carry_0_overflow(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x80,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_80_carry_0_overflow(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x80,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_81_carry_0_overflow(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x81,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FF_plus_7F_carry_0_overflow(setup):
    run_adc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_adc_binary_add_nmos_00_plus_80_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x80,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_80_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x80,
        True,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_81_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x81,
        True,
        0x83,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FF_plus_7F_carry_1(setup):
    run_adc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        True,
        0x7F,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


# Tests from latest test plan 2022-05-30
# May contain duplicates


def test_cpu_instruction_adc_binary_add_nmos_00_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x7F,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x80,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_00_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x00,
        0x81,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x7F,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x80,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_01_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x01,
        0x81,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x7F,
        False,
        0xFE,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x80,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x81,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x7F,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x80,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x81,
        False,
        0x01,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x7F,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x80,
        False,
        0x01,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x81,
        False,
        0x02,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x00,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_01_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x01,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_02_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0x02,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x00,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_01_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x01,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_02_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0x02,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_00_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x00,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_01_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x01,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_02_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0x02,
        False,
        0x83,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_FD_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0xFD,
        False,
        0x7C,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_FE_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0xFE,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_7F_plus_FF_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x7F,
        0xFF,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_FD_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0xFD,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_FE_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0xFE,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_80_plus_FF_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x80,
        0xFF,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_FD_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0xFD,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_FE_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0xFE,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_81_plus_FF_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0x81,
        0xFF,
        False,
        0x80,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FE_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFE,
        0x7F,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FE_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFE,
        0x80,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FE_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFE,
        0x81,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FF_plus_7F_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FF_plus_80_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFF,
        0x80,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_adc_binary_add_nmos_FF_plus_81_carry_0(setup):
    run_adc_test(
        "nmos",
        False,
        0xFF,
        0x81,
        False,
        0x80,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )
