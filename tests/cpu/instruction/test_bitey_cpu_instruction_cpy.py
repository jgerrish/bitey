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


def test_cpu_instruction_cpx_carry_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x02)

    # The CPY instruction
    computer.memory.write(0x00, 0xC0)
    computer.memory.write(0x01, 0x01)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["Y"] == 0x02

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x01

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is False


def test_cpu_instruction_cpx_compare_and_zero_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x02)

    # The CPY instruction
    computer.memory.write(0x00, 0xC0)
    computer.memory.write(0x01, 0x02)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["Y"] == 0x02

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x02

    # Check flags are correct
    assert computer.cpu.flags["C"].status is True
    assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is True


def test_cpu_instruction_cpx_negative_flag_true(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x01)

    # The CPY instruction
    computer.memory.write(0x00, 0xC0)
    computer.memory.write(0x01, 0x02)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.step(computer.memory)

    # Check accumulator wasn't modified
    assert computer.cpu.registers["Y"] == 0x01

    # Check memory wasn't modified
    assert computer.memory.read(0x01) == 0x02

    # Check flags are correct
    assert computer.cpu.flags["C"].status is False
    assert computer.cpu.flags["N"].status is True
    assert computer.cpu.flags["Z"].status is False
