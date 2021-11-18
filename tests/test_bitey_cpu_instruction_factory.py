from bitey.cpu.instruction.lda import LDA
from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.instruction.instruction_factory import InstructionFactory
from bitey.cpu.cpu import CPUJSONDecoder


def test_cpu_instruction_map():
    inst = InstructionFactory.get_instruction_from_opcode(173)
    assert inst == LDA


def test_cpu_builder():
    f = open("chip/6502.json")
    s = f.read()
    cpu_decoder = CPUJSONDecoder()
    cpu = cpu_decoder.decode(s)
    assert len(cpu.instructions.instructions) == 6

    inst = cpu.instructions.instructions[2]
    assert inst.name == "LDA"
    assert inst.opcodes.opcodes[0].opcode == 173
    assert inst.opcodes.opcodes[0].addressing_mode == AbsoluteAddressingMode()
    assert inst.description == "Load Accumulator with Memory"
