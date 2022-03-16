# Test the INC instructions (INC, INX, INY)
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


def test_inx(setup):
    "Test INX that doesn't wrap"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0x00)

    # The INX instruction
    computer.memory.write(0x00, 0xE8)
    computer.memory.write(0x01, 0xE8)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["X"].get() == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_inx_zero_flag_set(setup):
    "Test INX that wraps sets the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0xFF)
    assert computer.cpu.registers["X"].get() == 0xFF

    # The INX instruction
    computer.memory.write(0x00, 0xE8)
    computer.memory.write(0x01, 0xE8)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["X"].get() == 0x00
    assert computer.cpu.flags["Z"].status is True


def test_iny(setup):
    "Test INY that doesn't wrap"
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x00)

    # The INY instruction
    computer.memory.write(0x00, 0xC8)
    computer.memory.write(0x01, 0xC8)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["Y"].get() == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_iny_zero_flag_set(setup):
    "Test INY that wraps sets the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0xFF)
    assert computer.cpu.registers["Y"].get() == 0xFF

    # The INY instruction
    computer.memory.write(0x00, 0xC8)
    computer.memory.write(0x01, 0xC8)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["Y"].get() == 0x00
    assert computer.cpu.flags["Z"].status is True


def test_inc_zeropage(setup):
    "Test INY that doesn't wrap"
    computer = setup
    computer.reset()

    # The INC instruction
    computer.memory.write(0x00, 0xE6)
    # The zero page address to increment
    computer.memory.write(0x01, 0x10)
    # The value to increment
    computer.memory.write(0x10, 0x00)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.memory.read(0x10) == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_inc_zeropage_zero_flag_set(setup):
    "Test INC that wraps sets the Z flag"
    computer = setup
    computer.reset()

    # The INC instruction
    computer.memory.write(0x00, 0xE6)
    # The zero page address to increment
    computer.memory.write(0x01, 0x10)
    # The value to increment
    computer.memory.write(0x10, 0xFF)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.memory.read(0x10) == 0x00
    assert computer.cpu.flags["Z"].status is True
