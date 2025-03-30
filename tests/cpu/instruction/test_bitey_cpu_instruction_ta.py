import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ta import TAX
from bitey.cpu.instruction.ta import TAY
from bitey.cpu.instruction.ta import TXA
from bitey.cpu.instruction.ta import TYA


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(
    computer, opcode, instruction, expected_registers, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags

    try:
        instruction.execute(computer.cpu, computer.memory)
        for register, value in expected_registers:
            assert computer.cpu.registers[register].get() == value
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_tax(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x7A)

    i1_opcode = Opcode(0xAA, ImpliedAddressingMode())
    i1 = TAX("TAX", i1_opcode, "Transfer Accumulator to Index X")
    execute_instruction(computer, i1_opcode, i1, [("X", 0x7A)], False, False)


def test_cpu_instruction_tax_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0xBC)

    i1_opcode = Opcode(0xAA, ImpliedAddressingMode())
    i1 = TAX("TAX", i1_opcode, "Transfer Accumulator to Index X")
    execute_instruction(computer, i1_opcode, i1, [("X", 0xBC)], False, True)


def test_cpu_instruction_tax_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x00)
    computer.cpu.registers["X"].set(0xBC)

    i1_opcode = Opcode(0xAA, ImpliedAddressingMode())
    i1 = TAX("TAX", i1_opcode, "Transfer Accumulator to Index X")
    execute_instruction(computer, i1_opcode, i1, [("X", 0x00)], True, False)


def test_cpu_instruction_tay(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x7A)

    i1_opcode = Opcode(0xA8, ImpliedAddressingMode())
    i1 = TAY("TAY", i1_opcode, "Transfer Accumulator to Index Y")
    execute_instruction(computer, i1_opcode, i1, [("Y", 0x7A)], False, False)


def test_cpu_instruction_tay_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0xFA)

    i1_opcode = Opcode(0xA8, ImpliedAddressingMode())
    i1 = TAY("TAY", i1_opcode, "Transfer Accumulator to Index Y")
    execute_instruction(computer, i1_opcode, i1, [("Y", 0xFA)], False, True)


def test_cpu_instruction_tay_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x00)
    computer.cpu.registers["Y"].set(0xFA)

    i1_opcode = Opcode(0xA8, ImpliedAddressingMode())
    i1 = TAY("TAY", i1_opcode, "Transfer Accumulator to Index Y")
    execute_instruction(computer, i1_opcode, i1, [("Y", 0x00)], True, False)


def test_cpu_instruction_txa(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["X"].set(0x0B)

    i1_opcode = Opcode(0x8A, ImpliedAddressingMode())
    i1 = TXA("TXA", i1_opcode, "Transfer Index X to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0x0B)], False, False)


def test_cpu_instruction_txa_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["X"].set(0x8B)

    i1_opcode = Opcode(0x8A, ImpliedAddressingMode())
    i1 = TXA("TXA", i1_opcode, "Transfer Index X to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0x8B)], False, True)


def test_cpu_instruction_txa_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["X"].set(0x00)
    computer.cpu.registers["A"].set(0x8B)

    i1_opcode = Opcode(0x8A, ImpliedAddressingMode())
    i1 = TXA("TXA", i1_opcode, "Transfer Index X to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0x00)], True, False)


def test_cpu_instruction_tya(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["Y"].set(0x0B)

    i1_opcode = Opcode(0x98, ImpliedAddressingMode())
    i1 = TYA("TYA", i1_opcode, "Transfer Index Y to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0x0B)], False, False)


def test_cpu_instruction_tya_negative_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["Y"].set(0xBB)

    i1_opcode = Opcode(0x98, ImpliedAddressingMode())
    i1 = TYA("TYA", i1_opcode, "Transfer Index Y to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0xBB)], False, True)


def test_cpu_instruction_tya_zero_flag(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["Y"].set(0x00)
    computer.cpu.registers["A"].set(0xBB)

    i1_opcode = Opcode(0x98, ImpliedAddressingMode())
    i1 = TYA("TYA", i1_opcode, "Transfer Index Y to Accumulator")
    execute_instruction(computer, i1_opcode, i1, [("A", 0x00)], True, False)
