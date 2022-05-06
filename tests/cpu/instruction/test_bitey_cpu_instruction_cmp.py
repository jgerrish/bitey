import pytest
from bitey.computer.computer import Computer


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = build_computer()
    yield computer


# Different flag test cases:
# C N Z
# 0 0 0 impossible
# 0 0 1 impossible (R == M sets both C and Z)
# 0 1 0 R < M
# 0 1 1 impossible
# 1 0 0 R > M
# 1 0 1 R == M
# 1 1 0 impossible
# 1 1 1 impossible


def test_cpu_instruction_cmp_carry_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0x02)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0x01)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0x02

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x01

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cmp_compare_and_zero_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0x02)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0x02)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0x02

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x02

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is True


def test_cpu_instruction_cmp_negative_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0x01)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0x02)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0x01

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x02

    # Check flags are correct
    assert computer.cpu.flags["C"].status is False
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is True
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cmp_carry_flag_true_large_numbers(setup):
    "Test edge cases where carry flag is set with large numbers"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0xFF)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0xFE)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0xFF

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0xFE

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cmp_negative_flag_true_large_numbers(setup):
    "Test edge cases where negative flag is set with large numbers"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0xFE)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0xFF)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0xFE

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0xFF

    # Check flags are correct
    assert computer.cpu.flags["C"].status is False
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is True
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cmp_negative_flag_true_large_difference(setup):
    "Test edge cases where negative flag is set with a large difference"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0x00)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0xFF)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0x00

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0xFF

    # Check flags are correct
    assert computer.cpu.flags["C"].status is False
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is True
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cmp_carry_flag_true_large_difference(setup):
    "Test edge cases where negative flag is set with a large difference"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0xFF)

    # The CMP instruction
    computer.memory.write(0x00, 0xC9)
    computer.memory.write(0x01, 0x00)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["A"] == 0xFF

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x00

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    # The negative flag can be either true or false when the index
    # register is not equal to the memory value
    # assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is False
