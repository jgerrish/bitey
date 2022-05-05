import pytest

import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.cpu import CPU, StackOverflow

from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.txs import TXS


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def test_cpu_instruction_txs(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0xFF)

    assert computer.cpu.registers["S"].get() == 0x1FF

    i1_opcode = Opcode(0x9A, ImpliedAddressingMode())
    i1 = TXS("TXS", i1_opcode, "Transfer Index X to Stack Pointer")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("S", 0xFF)],
        [("C", False), ("Z", False), ("V", False), ("N", False)],
        [],
    )


def test_cpu_instruction_txs_stack_overflow(setup):
    "Test that a StackOverflow is still thrown after changing the stack pointer"
    computer = setup
    computer.reset()

    computer.cpu.registers["X"].set(0xFF)

    assert computer.cpu.registers["S"].get() == 0x1FF

    i1_opcode = Opcode(0x9A, ImpliedAddressingMode())
    i1 = TXS("TXS", i1_opcode, "Transfer Index X to Stack Pointer")

    tests.computer.computer.execute_explicit_instruction(
        computer,
        i1_opcode,
        i1,
        [("S", 0xFF)],
        [("C", False), ("Z", False), ("V", False), ("N", False)],
        [],
    )

    assert CPU.stack_start == 0x00FF

    try:
        for i in range(257):
            computer.cpu.stack_push(computer.memory, i)
        assert False
    except StackOverflow:
        assert True
