from dataclasses import dataclass
import json
from json import JSONDecoder


@dataclass
class Instruction:
    """
    A CPU instruction
    """

    "The name of the instruction"
    name: str

    "The instruction opcode"
    opcode: str

    "The instruction addressing mode"
    addressing_mode: str

    "A human-readable description of the instruction"
    description: str


@dataclass
class Instructions:
    """
    The collection of instructions this processor supports
    """

    instructions: list[Instruction]

    def __post_init__(self):
        "Create a dictionary so we can access registers by opcode"
        self.opcode_dict = {}
        for i in self.instructions:
            self.opcode_dict[i.opcode] = i

    def get_by_opcode(self, opcode):
        return self.opcode_dict[opcode]


class InstructionJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    """

    def decode(self, json_doc):
        if (
            ("name" in json_doc)
            and ("opcode" in json_doc)
            and ("addressing_mode" in json_doc)
            and ("description" in json_doc)
        ):
            return Instruction(
                json_doc["name"],
                json_doc["opcode"],
                json_doc["addressing_mode"],
                json_doc["description"],
            )
        else:
            # Return None if the instruction JSON object is missing fields or invalid
            return None


class InstructionsJSONDecoder(JSONDecoder):
    """
    Decode a list of register definitions in JSON format
    """

    def decode(self, json_doc):
        j = json.loads(json_doc)
        if "instructions" in j:
            instruction_list = []
            ijd = InstructionJSONDecoder()
            for instruction in j["instructions"]:
                i = ijd.decode(instruction)
                # Only append the instruction if all fields are present and the JSON
                # is valid for the instruction
                if i:
                    instruction_list.append(i)
            return Instructions(instruction_list)
