import pytest
import re
from bitey.computer.computer import Computer
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.sbc import SBCCMOS, SBCNMOS


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


def run_sbc_test(
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

    i1_opcode = Opcode(0xE9, ImmediateAddressingMode())
    if chip == "nmos":
        i1 = SBCNMOS("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")
    elif chip == "cmos":
        i1 = SBCCMOS("SBC", i1_opcode, "Subtract Memory from Accumulator with Borrow")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", expected_accumulator)],
        expected_flags,
        [],
    )


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
        # [("C", False), ("Z", True), ("V", False), ("N", False)],
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
        [("C", False), ("Z", False), ("V", False), ("N", True)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_00_minus_AA_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x00,
        0xAA,
        True,
        0xF0,
        [("C", False), ("Z", False), ("V", False), ("N", True)],
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
        # [("C", False), ("Z", False), ("V", False), ("N", True)],
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
        # [("C", False), ("Z", False), ("V", False), ("N", True)],
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
        [("C", False), ("Z", False), ("V", False), ("N", False)],
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


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_0(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x80,
        False,
        0x20,
        [("C", False), ("Z", False), ("V", True), ("N", False)],
    )


def test_cpu_instruction_sbc_decimal_subtract_nmos_01_minus_80_carry_1(setup):
    run_sbc_test(
        "nmos",
        True,
        0x01,
        0x80,
        True,
        0x21,
        [("C", False), ("Z", False), ("V", True), ("N", False)],
    )
