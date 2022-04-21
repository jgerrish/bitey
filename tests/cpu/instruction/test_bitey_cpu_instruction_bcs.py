import pytest
import tests.computer.computer
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_bcs_carry_flag_false(setup):
    "Test BCS when carry flag is False"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b01000000)
    computer.cpu.registers["PC"].set(0x00)

    # Accumulator ASL
    computer.memory.write(0x00, 0x0A)
    # BCS to relative address -2 (the ASL instruction)
    computer.memory.write(0x01, 0xB0)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["C"].status is False

    # BCS should continue
    assert computer.cpu.registers["PC"].get() == 0x03


def test_cpu_instruction_bcs_carry_flag_true(setup):
    "Test BCS when carry flag is True"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b10000000)
    computer.cpu.registers["PC"].set(0x00)

    # Accumulator ASL
    computer.memory.write(0x00, 0x0A)
    # BCS to relative address -2 (the ASL instruction)
    computer.memory.write(0x01, 0xB0)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["C"].status is True

    # BCS should jump
    assert computer.cpu.registers["PC"].get() == 0x00
