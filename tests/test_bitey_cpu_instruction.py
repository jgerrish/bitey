from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImpliedAddressingMode,
)
from bitey.cpu.cpu import CPU
from bitey.cpu.instruction.instruction import (
    Instruction,
    Instructions,
)
from bitey.cpu.instruction.opcode import Opcode, Opcodes
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
        return cpu.flags

    return None


def test_cpu_instruction_cli():
    flags = read_flags()
    assert flags["I"].status == 0
    flags["I"].set()
    assert flags["I"].status is True

    i1_opcodes = Opcodes([Opcode(88, ImpliedAddressingMode())])
    i1 = CLI("CLI", i1_opcodes, "Clear Interrupt Disable")
    i1.execute(flags, None, None)
    assert flags["I"].status is False


def test_cpu_instruction_sei():
    flags = read_flags()
    assert flags["I"].status is False

    i1_opcodes = Opcodes([Opcode(120, ImpliedAddressingMode())])
    i1 = SEI("SEI", i1_opcodes, "Set Interrupt Disable")
    i1.execute(flags, None, None)
    assert flags["I"].status is True
