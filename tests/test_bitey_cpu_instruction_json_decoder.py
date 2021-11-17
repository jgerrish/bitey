from bitey.cpu.instruction.instruction_json_decoder import (
    InstructionsJSONDecoder,
)


def test_cpu_instructions_json_decoder():
    f = open("chip/6502.json")
    s = f.read()
    i = InstructionsJSONDecoder()
    instructions = i.decode(s)
    assert len(instructions.instructions) == 2
