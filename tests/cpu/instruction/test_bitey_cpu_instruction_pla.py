import pytest
import tests.computer.computer
import tests.memory.memory


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_pha(setup):
    "Test PLA"
    computer = setup
    computer.reset()

    # Stack should be default
    assert computer.cpu.registers["S"].get() == 0xFF

    computer.cpu.registers["A"].set(0x49)
    computer.cpu.registers["PC"].set(0x00)

    # Use PHA to push the value before popping it

    # PHA
    computer.memory.write(0x00, 0x48)
    # PLA
    computer.memory.write(0x01, 0x68)
    # NOP
    computer.memory.write(0x02, 0xEA)

    # Step through 1 instruction
    computer.cpu.step(computer.memory)

    # Stack should be down one (one byte for accumulator)
    assert computer.cpu.registers["S"].get() == 0xFF - 0x001

    # Accumulator should have been pushed on the stack
    assert computer.memory.read(0x1FF) == 0x49

    # Pop the stack and test the accumulator
    computer.cpu.registers["A"].set(0x00)

    # Accumulator should be zero
    assert computer.cpu.registers["A"].get() == 0x00

    # Step through 1 instruction
    computer.cpu.step(computer.memory)

    # Stack should be the default
    assert computer.cpu.registers["S"].get() == 0xFF

    # Accumulator should be the popped value
    assert computer.cpu.registers["A"].get() == 0x49