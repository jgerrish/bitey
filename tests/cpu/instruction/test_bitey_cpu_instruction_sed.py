import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.sed import SED


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_sed(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["D"].clear()

    assert computer.cpu.flags["D"].status is False

    i1_opcode = Opcode(0xF8, ImpliedAddressingMode())
    i1 = SED("SED", i1_opcode, "Set Decimal Mode")
    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("D", True)], []
    )
