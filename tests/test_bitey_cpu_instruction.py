from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImpliedAddressingMode,
)
from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU
from bitey.cpu.instruction.instruction import (
    Instruction,
    Instructions,
    IncompleteInstruction,
)
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.cpu.instruction.brk import BRK
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.sei import SEI


def test_cpu_instruction_init():
    opcodes = Opcodes([Opcode(173, AbsoluteAddressingMode())])
    i = Instruction("LDA", opcodes, "Load Accumulator with Memory")
    assert i.name == "LDA"
    assert i.opcodes == opcodes
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instruction_init_no_type_checking():
    "We're not doing strict type checking yet, so this should pass"
    opcodes = Opcodes([Opcode(173, AbsoluteAddressingMode())])
    i = Instruction("LDA", opcodes, "Load Accumulator with Memory")
    assert i.name == "LDA"
    assert i.opcodes == opcodes
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instructions_init():
    i1_opcodes = Opcodes([Opcode(173, AbsoluteAddressingMode())])
    i1 = Instruction("LDA", i1_opcodes, "Load Accumulator with Memory")
    i2_opcodes = Opcodes([Opcode(141, AbsoluteAddressingMode())])
    i2 = Instruction("STA", i2_opcodes, "Store Accumulator in Memory")
    instructions = Instructions([i1, i2])
    assert len(instructions.instructions) == 2
    lda = instructions.get_by_opcode(173)
    assert lda == i1


def read_flags():
    with open("chip/6502.json") as f:
        chip_data = f.read()
        cpu = CPU.build_from_json(chip_data)
        cpu.flags.data = 0
        return cpu.flags

    return None


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_cpu_instruction_brk():
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["B"].status == 0

    assert flags["B"].flags == flags
    assert flags.data is not None

    # The reset code in the CPU loads the first instruction and
    # increments the PC by one
    # TODO: These tests should be simplified to not rely on that
    assert computer.cpu.registers["PC"].value == 1

    i1_opcodes = Opcodes([Opcode(0, ImpliedAddressingMode())])
    i1 = BRK("BRK", i1_opcodes, "Force Break")
    try:
        i1.execute(computer.cpu, computer.memory)
        assert False
    except IncompleteInstruction:
        assert True
        assert computer.cpu.flags["B"].status is True

        # The stack should be down three, two for the return address
        # and one for the flags
        assert computer.cpu.registers["S"].value == 0x01FC


def test_cpu_instruction_brk_from_memory():
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["B"].status == 0

    assert flags["B"].flags == flags
    assert flags.data is not None

    i1_opcodes = Opcodes([Opcode(0, ImpliedAddressingMode())])
    try:
        i1 = BRK("BRK", i1_opcodes, "Force Break")
        i1.execute(computer.cpu, computer.memory)
        assert False
    except IncompleteInstruction:
        assert True
        assert computer.cpu.flags["B"].status is True


def test_cpu_instruction_cli():
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["I"].status == 0

    assert flags["I"].flags == flags
    assert flags.data is not None

    flags["I"].set()
    assert flags["I"].status is True

    i1_opcodes = Opcodes([Opcode(88, ImpliedAddressingMode())])
    i1 = CLI("CLI", i1_opcodes, "Clear Interrupt Disable")
    i1.execute(computer.cpu, computer.memory)
    assert flags["I"].status is False


def test_cpu_instruction_sei():
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["I"].status is False

    i1_opcodes = Opcodes([Opcode(120, ImpliedAddressingMode())])
    i1 = SEI("SEI", i1_opcodes, "Set Interrupt Disable")
    i1.execute(computer.cpu, computer.memory)
    assert flags["I"].status is True
