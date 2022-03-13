from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.ld import LDA
from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.instruction.instruction_factory import InstructionFactory


def test_cpu_instruction_map():
    opcode = Opcode(173, AbsoluteAddressingMode())
    inst = InstructionFactory.get_instruction_from_opcode(opcode)
    assert inst == LDA


def test_cpu_instruction_factory_unimplemented():
    opcode = Opcode(111, AbsoluteAddressingMode())
    instruction = InstructionFactory.build("BLA", opcode, "BLA instruction")
    assert instruction.name == "BLA"
    assert instruction.opcode.opcode == 111
    assert instruction.opcode.addressing_mode == AbsoluteAddressingMode()
    assert instruction.description == "BLA instruction"


def test_cpu_instruction_factory_implemented():
    opcode = Opcode(173, AbsoluteAddressingMode())
    instruction = InstructionFactory.build(
        "LDA", opcode, "Load Accumulator with Memory"
    )
    assert isinstance(instruction, LDA)
    assert instruction.name == "LDA"
    assert instruction.opcode.opcode == 173
    assert instruction.opcode.addressing_mode == AbsoluteAddressingMode()
    assert instruction.description == "Load Accumulator with Memory"
