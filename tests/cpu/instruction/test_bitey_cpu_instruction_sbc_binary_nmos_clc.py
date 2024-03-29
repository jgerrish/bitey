import pytest
import tests.computer.computer
from tests.computer.computer import run_sbc_test
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_sbc_binary_subtract_nmos_00_minus_80_carry_0_overflow(setup):
    run_sbc_test(
        "nmos",
        False,
        0x00,
        0x80,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_80_carry_0_overflow(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x80,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_81_carry_0_overflow(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x81,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FF_minus_7F_carry_0_overflow(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


# Test edge cases for overflow flag
# Test no-carry CLC mode


def test_cpu_instruction_sbc_binary_subtract_nmos_00_minus_80_carry_1(setup):
    run_sbc_test(
        "nmos",
        False,
        0x00,
        0x80,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_80_carry_1(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x80,
        True,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_81_carry_1(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x81,
        True,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FF_minus_7F_carry_1(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        True,
        0x80,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


# Tests from latest test plan 2022-05-30
# May contain duplicates


def test_cpu_instruction_sbc_binary_subtract_nmos_00_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x00,
        0x7F,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_00_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x00,
        0x80,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_00_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x00,
        0x81,
        False,
        0x7E,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x7F,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x80,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_01_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x01,
        0x81,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x7F,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x80,
        False,
        0xFE,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x81,
        False,
        0xFD,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x7F,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x80,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x81,
        False,
        0xFE,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x7F,
        False,
        0x01,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x80,
        False,
        0x00,
        [("C", True), ("Z", True), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x81,
        False,
        0xFF,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x00,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_01_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x01,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_02_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0x02,
        False,
        0x7C,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x00,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_01_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x01,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_02_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0x02,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_00_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x00,
        False,
        0x80,
        [("C", True), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_01_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x01,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_02_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0x02,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_FD_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0xFD,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_FE_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0xFE,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", True), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_7F_minus_FF_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x7F,
        0xFF,
        False,
        0x7F,
        [("C", False), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_FD_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0xFD,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_FE_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0xFE,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_80_minus_FF_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x80,
        0xFF,
        False,
        0x80,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_FD_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0xFD,
        False,
        0x83,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_FE_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0xFE,
        False,
        0x82,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_81_minus_FF_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0x81,
        0xFF,
        False,
        0x81,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FE_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFE,
        0x7F,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FE_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFE,
        0x80,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FE_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFE,
        0x81,
        False,
        0x7C,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FF_minus_7F_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFF,
        0x7F,
        False,
        0x7F,
        [("C", True), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FF_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFF,
        0x80,
        False,
        0x7E,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )


def test_cpu_instruction_sbc_binary_subtract_nmos_FF_minus_81_carry_0(setup):
    run_sbc_test(
        "nmos",
        False,
        0xFF,
        0x81,
        False,
        0x7D,
        [("C", True), ("Z", False), ("V", False), ("N", False)],
    )
