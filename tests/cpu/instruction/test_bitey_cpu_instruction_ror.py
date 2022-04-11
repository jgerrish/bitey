import pytest
import re
from bitey.computer.computer import Computer
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import AccumulatorAddressingMode
from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ror import ROR


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


def execute_instruction(
    computer, opcode, expected_a_register, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = ROR("ROR", opcode, "Rotate One Bit ROR (Memory or Accumulator)")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].get() == expected_a_register
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_ror_no_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b00101100)

    i1_opcode = Opcode(0x6A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b00010110, False, False)


def test_cpu_instruction_ror_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.flags["C"].set()
    computer.cpu.registers["A"].set(0b00101100)

    i1_opcode = Opcode(0x6A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10010110, False, True)


def test_cpu_instruction_ror_carry_set(setup):
    computer = setup
    computer.reset()

    assert computer.cpu.flags["C"].status is False
    computer.cpu.registers["A"].set(0b10101101)

    i1_opcode = Opcode(0x6A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01010110, False, False)
    assert computer.cpu.flags["C"].status is True


def test_cpu_instruction_ror_negative_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.flags["C"].set()
    computer.cpu.registers["A"].set(0b01101100)

    i1_opcode = Opcode(0x6A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b10110110, False, True)


def test_cpu_instruction_ror_zero_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b00000001)

    i1_opcode = Opcode(0x6A, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b00000000, True, False)


def test_cpu_instruction_ror_zeropage_no_carry(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b00101100)]
    )

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b00010110)], False, False, False
    )


def test_cpu_instruction_ror_zeropage_carry(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b00101100)]
    )

    computer.cpu.flags["C"].set()
    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b10010110)], False, True, False
    )


def test_cpu_instruction_ror_zeropage_carry_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b10101101)]
    )

    assert computer.cpu.flags["C"].status is False

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b01010110)], False, False, True
    )


def test_cpu_instruction_ror_zeropage_negative_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b01101100)]
    )

    computer.cpu.flags["C"].set()
    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b10110110)], False, True, False
    )


def test_cpu_instruction_ror_zeropage_zero_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b00000001)]
    )

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b00000000)], True, False, True
    )


def test_cpu_instruction_ror_bug_no_carry():
    "Test quirky ROR instruction that doesn't carry"
    computer = build_computer("kim-1")
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x66), (0x01, 0x02), (0x02, 0b10101101)]
    )

    assert computer.cpu.flags["C"].status is False

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b01010110)], False, False, False
    )
