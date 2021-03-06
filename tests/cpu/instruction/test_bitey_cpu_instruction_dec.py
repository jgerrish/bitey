# Test the DEC instructions (DEC, DEX, DEY)
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


def test_dex(setup):
    "Test DEX that doesn't wrap"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0x02)

    # The DEX instruction
    computer.memory.write(0x00, 0xCA)
    computer.memory.write(0x01, 0xCA)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["X"].get() == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_dex_zero_flag_set(setup):
    "Test DEX that setting to zero sets the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0x01)

    # The DEX instruction
    computer.memory.write(0x00, 0xCA)
    computer.memory.write(0x01, 0xCA)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["X"].get() == 0x00
    assert computer.cpu.flags["Z"].status is True


def test_dex_wrap_zero_flag_not_set(setup):
    "Test DEX that wrapping does not set the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0x00)

    # The DEX instruction
    computer.memory.write(0x00, 0xCA)
    computer.memory.write(0x01, 0xCA)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["X"].get() == 0xFF
    assert computer.cpu.flags["Z"].status is False


def test_dey(setup):
    "Test DEY that doesn't wrap"
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x02)

    # The DEY instruction
    computer.memory.write(0x00, 0x88)
    computer.memory.write(0x01, 0x88)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["Y"].get() == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_dey_zero_flag_set(setup):
    "Test DEY that setting to zero sets the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x01)

    # The DEY instruction
    computer.memory.write(0x00, 0x88)
    computer.memory.write(0x01, 0x88)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["Y"].get() == 0x00
    assert computer.cpu.flags["Z"].status is True


def test_dey_wraps_zero_flag_not_set(setup):
    "Test DEY that wrapping doesn't set the Z flag"
    computer = setup
    computer.reset()

    computer.cpu.registers["Y"].set(0x00)

    # The DEY instruction
    computer.memory.write(0x00, 0x88)
    computer.memory.write(0x01, 0x88)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.cpu.registers["Y"].get() == 0xFF
    assert computer.cpu.flags["Z"].status is False


def test_dec_zeropage(setup):
    "Test DEY that doesn't set zero flag"
    computer = setup
    computer.reset()

    # The DEC instruction
    computer.memory.write(0x00, 0xC6)
    # The zero page address to decrement
    computer.memory.write(0x01, 0x10)
    # The value to decrement
    computer.memory.write(0x10, 0x02)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.memory.read(0x10) == 0x01
    assert computer.cpu.flags["Z"].status is False


def test_dec_zeropage_zero_flag_set(setup):
    "Test DEC that wraps sets the Z flag"
    computer = setup
    computer.reset()

    # The DEC instruction
    computer.memory.write(0x00, 0xC6)
    # The zero page address to decrement
    computer.memory.write(0x01, 0x10)
    # The value to decrement
    computer.memory.write(0x10, 0x01)

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.get_next_instruction(computer.memory)
    computer.cpu.execute_instruction(computer.memory)

    assert computer.memory.read(0x10) == 0x00
    assert computer.cpu.flags["Z"].status is True
