import json
from json import JSONDecoder

from bitey.cpu.instruction.instruction import (
    Instructions,
)

from bitey.cpu.addressing_mode_factory import AddressingModeFactory
from bitey.cpu.instruction.instruction_factory import InstructionFactory


class InstructionJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    The instance generation logic is collected in here, it should be refactored
    to the other classes.
    """

    def decode(self, json_doc):
        if (
            ("name" in json_doc)
            and ("opcode" in json_doc)
            and ("addressing_mode" in json_doc)
            and ("description" in json_doc)
        ):
            name = json_doc["name"]
            opcode = json_doc["opcode"]
            addressing_mode_str = json_doc["addressing_mode"]
            description = json_doc["description"]
            addressing_mode = AddressingModeFactory.build(addressing_mode_str)

            return InstructionFactory.build(name, opcode, addressing_mode, description)

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
