import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.cli import CLI


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_cli(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["I"].set()

    assert computer.cpu.flags["I"].status is True

    i1_opcode = Opcode(0x58, ImpliedAddressingMode())
    i1 = CLI("CLI", i1_opcode, "Clear Interrupt Disable Bit")
    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("I", False)], []
    )
