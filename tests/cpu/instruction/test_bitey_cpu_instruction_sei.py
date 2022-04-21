import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.sei import SEI


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_sei(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["I"].clear()

    assert computer.cpu.flags["I"].status is False

    i1_opcode = Opcode(0x78, ImpliedAddressingMode())
    i1 = SEI("SEI", i1_opcode, "Set Interrupt Disable Bit")
    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("I", True)], []
    )
