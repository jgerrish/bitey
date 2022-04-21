import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.cld import CLD


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_cld(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["D"].set()

    assert computer.cpu.flags["D"].status is True

    i1_opcode = Opcode(0xD8, ImpliedAddressingMode())
    i1 = CLD("CLD", i1_opcode, "Clear Decimal Mode")
    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("D", False)], []
    )
