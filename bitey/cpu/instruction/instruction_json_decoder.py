import json
from json import JSONDecoder

from bitey.cpu.instruction.opcode import OpcodesJSONDecoder
from bitey.cpu.instruction.instruction import (
    Instructions,
)

from bitey.cpu.instruction.instruction_factory import InstructionFactory


class InstructionJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    The instance generation logic is collected in here, it should be refactored
    to the other classes.
    """

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        if ("name" in parsed_json) and ("description" in parsed_json):
            name = parsed_json["name"]
            description = parsed_json["description"]
            if "opcodes" in parsed_json:
                opcodes_decoder = OpcodesJSONDecoder()
                opcodes = opcodes_decoder.decode_parsed(parsed_json["opcodes"])
            else:
                opcodes = None

            return InstructionFactory.build(name, opcodes, description)

        else:
            # Return None if the instruction JSON object is missing fields or invalid
            return None


class InstructionsJSONDecoder(JSONDecoder):
    """
    Decode a list of register definitions in JSON format
    """

    # TODO: Define this format formally
    # TODO: Extend to allow multiple address modes in the instruction definitions

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        instruction_list = []
        ijd = InstructionJSONDecoder()
        for instruction in parsed_json:
            i = ijd.decode_parsed(instruction)
            # Only append the instruction if all fields are present and the JSON
            # is valid for the instruction
            if i:
                instruction_list.append(i)
        return Instructions(instruction_list)
