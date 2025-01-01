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


def test_build_cpu_instruction_brk(setup):
    "Test the BRK instruction"
    computer = setup

    # BRK instructions
    computer.memory.write(0x00, 0x00)
    computer.memory.write(0x01, 0xEA)
    # The interrupt vector pointer
    computer.memory.write(0xFFFE, 0x10)
    computer.memory.write(0xFFFF, 0x20)

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.registers["PC"].get() == 0x00

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x2010
    # Stack should be down three (two bytes for address, one for
    # process status register)
    assert computer.cpu.registers["S"] == 0xFF - 0x003

    assert computer.memory.read(0x1FF) == 0x00
    assert computer.memory.read(0x1FE) == 0x02
    # Interrupt Disable, Break and Expansion should be set
    assert computer.memory.read(0x1FD) == 0b00110000
