import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.clc import CLC


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_clc(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["C"].set()

    assert computer.cpu.flags["C"].status is True

    i1_opcode = Opcode(0x18, ImpliedAddressingMode())
    i1 = CLC("CLC", i1_opcode, "Clear Carry Flag")
    tests.computer.computer.execute_explicit_instruction(
        computer, i1_opcode, i1, [], [("C", False)]
    )
