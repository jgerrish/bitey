from bitey.cpu.instruction.lda import LDA
from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.instruction.instruction_factory import InstructionFactory
from bitey.cpu.instruction.instruction_json_decoder import (
    InstructionsJSONDecoder,
)


def test_cpu_instruction_map():
    inst = InstructionFactory.get_instruction_from_opcode(173)
    assert inst == LDA


def test_cpu_builder():
    f = open("chip/6502.json")
    s = f.read()
    i = InstructionsJSONDecoder()
    instructions = i.decode(s)
    assert len(instructions.instructions) == 2

    inst = instructions.instructions[0]
    assert inst.name == "LDA"
    assert inst.opcode == 173
    assert inst.addressing_mode == AbsoluteAddressingMode()
    assert inst.description == "Load Accumulator with Memory"
