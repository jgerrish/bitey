import pytest

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
import tests.computer.computer
import tests.memory.memory

from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.tsx import TSX


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(
    computer, opcode, expected_x_register, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = TSX("TSX", opcode, "Transfer Stack Pointer to Index X")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["X"].get() == expected_x_register
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_tsx(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["S"].set(0x34)

    i1_opcode = Opcode(0xBA, ImpliedAddressingMode())
    execute_instruction(computer, i1_opcode, 0x34, False, False)


def test_cpu_instruction_tsx_n_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["S"].set(0xB4)

    i1_opcode = Opcode(0xBA, ImpliedAddressingMode())
    execute_instruction(computer, i1_opcode, 0xB4, False, True)


def test_cpu_instruction_tsx_z_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["S"].set(0x00)

    i1_opcode = Opcode(0xBA, ImpliedAddressingMode())
    execute_instruction(computer, i1_opcode, 0x00, True, False)


def test_cpu_instruction_tsx_memory(setup):
    computer = setup
    computer.reset()

    # The TSX instruction
    computer.memory.write(0x00, 0xBA)
    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["S"].set(0x34)

    computer.cpu.step(computer.memory)

    # Check registers are correct
    assert computer.cpu.registers["X"].get() == 0x34

    # Check flags are correct
    assert computer.cpu.flags["N"].status is False
    assert computer.cpu.flags["Z"].status is False
