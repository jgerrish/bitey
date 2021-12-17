from bitey.cpu.addressing_mode import ImpliedAddressingMode
from bitey.cpu.instruction.opcode import Opcode, Opcodes
from bitey.cpu.instruction.instruction_json_decoder import (
    InstructionJSONDecoder,
    InstructionClassJSONDecoder,
    InstructionSetJSONDecoder,
)


def test_cpu_instruction_json_decoder():
    json_string = """
    {
        "name": "TXS",
        "description": "Transfer index X to stack pointer",
        "opcode":
            {
                "opcode": 154,
                "addressing_mode": "implied"
            }
    }
    """

    instruction_decoder = InstructionJSONDecoder()
    instruction = instruction_decoder.decode(json_string)
    assert instruction is not None
    assert instruction.name == "TXS"
    opcode = Opcode(154, ImpliedAddressingMode())
    assert instruction.opcode == opcode


def test_cpu_instruction_class_json_decoder():
    json_string = """
    {
        "name": "TXS",
        "description": "Transfer index X to stack pointer",
        "opcodes": [
            {
                "opcode": 154,
                "addressing_mode": "implied"
            }
        ]
    }
    """

    instruction_class_decoder = InstructionClassJSONDecoder()
    instruction_class = instruction_class_decoder.decode(json_string)
    assert instruction_class is not None
    assert instruction_class.name == "TXS"
    opcodes = Opcodes([Opcode(154, ImpliedAddressingMode())])
    assert instruction_class.opcodes == opcodes


def test_cpu_instruction_set_json_decoder():
    json_string = """
    [
        {
            "name": "TXS",
            "description": "Transfer index X to stack pointer",
            "opcodes": [
                {
                    "opcode": 154,
                    "addressing_mode": "implied"
                }
            ]
        }
    ]
    """
    i = InstructionSetJSONDecoder()
    instruction_set = i.decode(json_string)
    assert len(instruction_set.instructions) == 1
