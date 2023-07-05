import re
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.addressing_mode import ImmediateAddressingMode
from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.computer.computer import Computer
from bitey.cpu.instruction.adc import ADCCMOS, ADCNMOS
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


# def build_computer():
#     "Build the computer"
#     computer = None

#     with open("chip/6502.json") as f:
#         chip_data = f.read()
#         computer = Computer.build_from_json(chip_data)
#         return computer

#     return None


def init_computer():
    "Initialize computer for tests"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    assert computer.cpu.registers["PC"].get() == 0x01

    return computer


def execute_instruction(
    computer,
    expected_memory,
    expected_z_flag,
    expected_n_flag,
    expected_c_flag,
):
    """
    Execute an instruction fetched from the PC and test memory and flags
    """
    flags = computer.cpu.flags
    computer.cpu.registers["PC"].set(0x00)

    try:
        computer.step()
        # Test that the memory is written correctly
        for mem in expected_memory:
            assert computer.memory.read(mem[0]) == mem[1]

        # Test the flags
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
        assert flags["C"].status is expected_c_flag
    except IncompleteInstruction:
        assert False


def execute_explicit_instruction(
    computer, opcode, instruction, expected_registers, expected_flags, expected_memory
):
    "Execute an explicit instruction based on an opcode"
    flags = computer.cpu.flags

    try:
        instruction.execute(computer.cpu, computer.memory)
        for register, value in expected_registers:
            assert (
                computer.cpu.registers[register].get() == value
            ), "register {} should be {}, but was {}".format(
                register, value, computer.cpu.registers[register].get()
            )
        for flag, value in expected_flags:
            assert (
                flags[flag].status is value
            ), "flag {} should be {}, but was {}".format(
                flag, value, flags[flag].status
            )
        for address, value in expected_memory:
            assert (
                computer.memory.read(address) == value
            ), "memory {} should be {}, but was {}".format(
                address, value, computer.memory.read(address)
            )
    except IncompleteInstruction:
        assert False


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

    execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", expected_accumulator)],
        expected_flags,
        [],
    )


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

    execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("A", expected_accumulator)],
        expected_flags,
        [],
    )
