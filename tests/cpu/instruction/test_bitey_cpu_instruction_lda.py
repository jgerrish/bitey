from bitey.cpu.addressing_mode import (
    ImmediateAddressingMode,
    ZeroPageAddressingMode,
)
from bitey.computer.computer import Computer
from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.lda import LDA


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_cpu_instruction_lda_immediate():
    "Test LDA in immediate addressing mode that doesn't load a zero"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].value == 1

    computer.memory.write(1, 0x2B)

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    i1 = LDA("LDA", i1_opcode, "Load Accumulator with Memory")
    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"] == 0x2B
        assert flags["Z"].status is False
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_lda_immediate_zero():
    "Test LDA in immediate addressing mode that loads a zero"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].value == 1

    computer.memory.write(1, 0x00)

    i1_opcode = Opcode(169, ImmediateAddressingMode())
    i1 = LDA("LDA", i1_opcode, "Load Accumulator with Memory")
    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].value == 0x00
        assert flags["Z"].status is True
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_lda_zeropage():
    "Test LDA in zero page addressing mode that doesn't load a zero"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].value == 1

    computer.memory.write(0x01, 0x2B)
    computer.memory.write(0x2B, 0x55)

    i1_opcode = Opcode(165, ZeroPageAddressingMode())
    i1 = LDA("LDA", i1_opcode, "Load Accumulator with Memory")
    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"] == 0x55
        assert flags["Z"].status is False
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_lda_zeropage_zero():
    "Test LDA in zero page addressing mode that loads a zero"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].value == 1

    computer.memory.write(0x01, 0x2B)
    computer.memory.write(0x2B, 0x00)

    i1_opcode = Opcode(169, ZeroPageAddressingMode())
    i1 = LDA("LDA", i1_opcode, "Load Accumulator with Memory")
    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].value == 0x00
        assert flags["Z"].status is True
    except IncompleteInstruction:
        assert False
