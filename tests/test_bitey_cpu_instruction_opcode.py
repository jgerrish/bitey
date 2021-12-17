from bitey.cpu.addressing_mode import ImpliedAddressingMode

from bitey.cpu.instruction.opcode import (
    Opcode,
    OpcodeJSONDecoder,
    OpcodesJSONDecoder,
)


def test_cpu_instruction_opcode_init():
    opcode = Opcode(0, ImpliedAddressingMode())

    assert opcode.opcode == 0
    assert opcode.addressing_mode == ImpliedAddressingMode()


def test_cpu_instruction_opcode_json_decoder():
    json_string = '{ "opcode": 154, "addressing_mode": "implied" }'
    opcode_decoder = OpcodeJSONDecoder()
    opcode = opcode_decoder.decode(json_string)

    assert opcode.opcode == 154
    assert opcode.addressing_mode == ImpliedAddressingMode()


def test_cpu_instruction_opcodes_json_decoder():
    json_string = '[ { "opcode": 154, "addressing_mode": "implied" } ]'

    opcodes_decoder = OpcodesJSONDecoder()
    opcodes = opcodes_decoder.decode(json_string)

    assert opcodes is not None
    assert len(opcodes.opcodes) == 1
    assert 154 in opcodes
    assert opcodes[154].opcode == 154
    assert opcodes[154].addressing_mode == ImpliedAddressingMode()
