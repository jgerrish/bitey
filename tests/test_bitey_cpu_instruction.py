from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    AbsoluteXAddressingMode,
    AbsoluteYAddressingMode,
    AccumulatorAddressingMode,
    ImmediateAddressingMode,
    ImpliedAddressingMode,
    IndexedIndirectAddressingMode,
    IndirectIndexedAddressingMode,
    RelativeAddressingMode,
    ZeroPageAddressingMode,
    ZeroPageXAddressingMode,
    ZeroPageYAddressingMode,
)
from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU
from bitey.cpu.instruction.instruction import (
    Instruction,
    InstructionClass,
    Instructions,
    InstructionSet,
    IncompleteInstruction,
)
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.cpu.instruction.brk import BRK
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.lda import LDA
from bitey.cpu.instruction.sei import SEI


def test_cpu_instruction_init():
    opcode = Opcode(173, AbsoluteAddressingMode())
    i = Instruction("LDA", opcode, "Load Accumulator with Memory")
    assert i.name == "LDA"
    assert i.opcode == opcode
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instruction_init_no_type_checking():
    "We're not doing strict type checking yet, so this should pass"
    opcode = Opcode(173, AbsoluteAddressingMode())
    i = Instruction("LDA", opcode, "Load Accumulator with Memory")
    assert i.name == "LDA"
    assert i.opcode == opcode
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instructions_init():
    i1_opcode = Opcode(173, AbsoluteAddressingMode())
    i1 = Instruction("LDA", i1_opcode, "Load Accumulator with Memory")
    i2_opcode = Opcode(141, AbsoluteAddressingMode())
    i2 = Instruction("STA", i2_opcode, "Store Accumulator in Memory")
    instructions = Instructions([i1, i2])
    assert len(instructions.instructions) == 2

    lda = instructions.get_by_opcode(173)
    assert lda == i1


def test_cpu_instruction_class_init():
    i1_opcode_1 = Opcode(173, AbsoluteAddressingMode())
    i1_opcode_2 = Opcode(165, ZeroPageAddressingMode())
    i1 = Instruction("LDA", i1_opcode_1, "Load Accumulator with Memory")
    opcodes = Opcodes([i1_opcode_1, i1_opcode_2])
    instruction_class = InstructionClass(
        "LDA", i1, opcodes, "Load Accumulator with Memory"
    )

    assert instruction_class.name == "LDA"
    assert len(instruction_class.opcodes) == 2
    assert instruction_class.description == "Load Accumulator with Memory"


def test_cpu_instruction_set_init():
    i1_opcode_1 = Opcode(173, AbsoluteAddressingMode())
    i1_opcode_2 = Opcode(165, ZeroPageAddressingMode())
    i1 = Instruction("LDA", i1_opcode_1, "Load Accumulator with Memory")
    opcodes = Opcodes([i1_opcode_1, i1_opcode_2])
    instruction_class = InstructionClass(
        "LDA", i1, opcodes, "Load Accumulator with Memory"
    )

    instruction_set = InstructionSet([instruction_class])

    assert instruction_set.instructions[0].name == "LDA"
    assert len(instruction_set.instructions[0].opcodes) == 2
    assert instruction_set.instructions[0].description == "Load Accumulator with Memory"


def test_cpu_instruction_short_str():
    opcode = Opcode(0x58, ImpliedAddressingMode())
    cli = CLI("CLI", opcode, "Clear Interrupt Disable")
    assert cli.short_str() == "CLI"


def test_cpu_instruction_assembly_str():
    computer = build_computer()

    # Set the PC
    computer.cpu.registers["PC"].set(0x00)

    # Set the X register
    computer.cpu.registers["X"].set(0x4A)

    # Set the Y register
    computer.cpu.registers["Y"].set(0xEC)

    # Implied mode CLI instruction
    computer.memory.write(0x00, 0x58)
    opcode = Opcode(0x58, ImpliedAddressingMode())
    cli = CLI("CLI", opcode, "Clear Interrupt Disable")
    assert cli.assembly_str(computer) == "CLI"

    # Immediate mode LDA
    computer.memory.write(0x01, 0xA9)
    opcode = Opcode(0xA9, ImmediateAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    computer.cpu.registers["PC"].inc()
    assert lda.assembly_str(computer) == "LDA  #$a9"

    # ZeroPage mode LDA
    computer.memory.write(0x02, 0x99)
    opcode = Opcode(0xA5, ZeroPageAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    computer.cpu.registers["PC"].set(0x02)
    assert lda.assembly_str(computer) == "LDA  $99"

    # Absolute addressing mode LDA
    computer.memory.write(0x03, 0x5C)
    computer.memory.write(0x04, 0xB4)
    opcode = Opcode(0xAD, AbsoluteAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    computer.cpu.registers["PC"].set(0x03)
    assert lda.assembly_str(computer) == "LDA  $b45c"

    # Accumulator addressing mode
    opcode = Opcode(0x0A, AccumulatorAddressingMode())
    asl = Instruction("ASL", opcode, "Shift Left One Bit (Memory or Accumulator")
    assert asl.assembly_str(computer) == "ASL"

    # AbsoluteX addressing mode
    computer.memory.write(0x05, 0x0F)
    computer.memory.write(0x06, 0xF7)
    opcode = Opcode(0xBD, AbsoluteXAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    computer.cpu.registers["PC"].set(0x05)
    assert lda.assembly_str(computer) == "LDA  $f70f,X"

    # AbsoluteY addressing mode
    computer.memory.write(0x07, 0x13)
    computer.memory.write(0x08, 0x16)
    opcode = Opcode(0xB9, AbsoluteYAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    assert lda.assembly_str(computer) == "LDA  $1613,Y"

    # IndexedIndirect addressing mode
    computer.memory.write(0x09, 0x30)
    opcode = Opcode(0xA1, IndexedIndirectAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    assert lda.assembly_str(computer) == "LDA  ($30,X)"

    # IndirectIndexed addressing mode
    computer.memory.write(0x0A, 0x4C)
    opcode = Opcode(0xB1, IndirectIndexedAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    assert lda.assembly_str(computer) == "LDA  ($4c),Y"

    # ZeroPageX addressing mode
    computer.memory.write(0x0B, 0xAC)
    opcode = Opcode(0xB5, ZeroPageXAddressingMode())
    lda = LDA("LDA", opcode, "Load Accumulator with Memory")
    assert lda.assembly_str(computer) == "LDA  $ac,X"

    # ZeroPageY addressing mode
    computer.memory.write(0x0C, 0xEC)
    opcode = Opcode(0xB1, ZeroPageYAddressingMode())
    lda = Instruction("LDX", opcode, "Load Index X with Memory")
    assert lda.assembly_str(computer) == "LDX  $ec,Y"

    # Relative addressing mode
    computer.memory.write(0x0D, 0xA3)
    opcode = Opcode(0xB0, RelativeAddressingMode())
    lda = Instruction("BCS", opcode, "Branch on Carry Set")
    assert lda.assembly_str(computer) == "BCS  $ffb0"


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
    assert computer.cpu.registers["PC"].value == 0x01

    i1_opcode = Opcode(0, ImpliedAddressingMode())
    i1 = BRK("BRK", i1_opcode, "Force Break")
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

    i1_opcode = Opcode(0, ImpliedAddressingMode())
    try:
        i1 = BRK("BRK", i1_opcode, "Force Break")
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

    i1_opcode = Opcode(88, ImpliedAddressingMode())
    i1 = CLI("CLI", i1_opcode, "Clear Interrupt Disable")
    i1.execute(computer.cpu, computer.memory)
    assert flags["I"].status is False


def test_cpu_instruction_sei():
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["I"].status is False

    i1_opcode = Opcode(120, ImpliedAddressingMode())
    i1 = SEI("SEI", i1_opcode, "Set Interrupt Disable")
    i1.execute(computer.cpu, computer.memory)
    assert flags["I"].status is True
