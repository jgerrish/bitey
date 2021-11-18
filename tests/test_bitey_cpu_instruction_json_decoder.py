from bitey.cpu.instruction.instruction_json_decoder import (
    InstructionJSONDecoder,
    InstructionsJSONDecoder,
)


def test_cpu_instruction_opcode_json_decoder():
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

    instruction_decoder = InstructionJSONDecoder()
    instruction = instruction_decoder.decode(json_string)
    assert instruction is not None
    assert instruction.name == "TXS"
    assert len(instruction.opcodes) == 1


def test_cpu_instructions_json_decoder():
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
    i = InstructionsJSONDecoder()
    instructions = i.decode(json_string)
    assert len(instructions.instructions) == 1
