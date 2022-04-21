import pytest
import tests.computer.computer
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_bvs_overflow_flag_false(setup):
    "Test BVS when overflow flag is False"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b00000000)
    computer.cpu.registers["PC"].set(0x00)

    # Accumulator ASL
    computer.memory.write(0x00, 0x0A)
    # BVS to relative address -2 (the ASL instruction)
    computer.memory.write(0x01, 0x70)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["V"].status is False

    # BVS should continue
    assert computer.cpu.registers["PC"].get() == 0x03


def test_cpu_instruction_bvs_overflow_flag_true(setup):
    "Test BVS when overflow flag is True"
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b00000000)
    computer.cpu.registers["PC"].set(0x00)

    # Accumulator ASL
    computer.memory.write(0x00, 0x0A)
    # BVS to relative address -2 (the ASL instruction)
    computer.memory.write(0x01, 0x70)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Directly set the overflow flag
    computer.cpu.flags["V"].set(True)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["V"].status is True

    # BVS should jump
    assert computer.cpu.registers["PC"].get() == 0x00
