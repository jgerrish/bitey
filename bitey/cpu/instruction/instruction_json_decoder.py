import json
from json import JSONDecoder

from bitey.cpu.instruction.opcode import OpcodeJSONDecoder, OpcodesJSONDecoder
from bitey.cpu.instruction.instruction import Instructions, InstructionSet

from bitey.cpu.instruction.instruction_factory import (
    InstructionFactory,
    InstructionClassFactory,
)


class InstructionJSONDecoder(JSONDecoder):
    """
    Decode an instruction definition in JSON format.
    The instance generation logic is collected in here, it should be
    refactored to the other classes.
    """

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        if ("name" in parsed_json) and ("description" in parsed_json):
            name = parsed_json["name"]
            description = parsed_json["description"]
            if "opcode" in parsed_json:
                opcode_decoder = OpcodeJSONDecoder()
                opcode = opcode_decoder.decode_parsed(parsed_json["opcode"])
            else:
                opcode = None

            print("opcode: {}".format(opcode))
            return InstructionFactory.build(name, opcode, description)

        else:
            # Return None if the instruction JSON object is missing fields or invalid
            return None


class InstructionClassJSONDecoder(JSONDecoder):
    """
    Decode an instruction class definition in JSON format.
    The instance generation logic is collected in here, it should be
    refactored to the other classes.
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

            icf = InstructionClassFactory.build(name, opcodes, description)
            return icf

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


class InstructionSetJSONDecoder(JSONDecoder):
    """
    Decode a list of instruction class definitions in JSON format
    """

    # TODO: Define this format formally

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        instruction_list = []
        ijd = InstructionClassJSONDecoder()
        for instruction in parsed_json:
            i = ijd.decode_parsed(instruction)
            # Only append the instruction if all fields are present and the JSON
            # is valid for the instruction
            if i:
                instruction_list.append(i)
        return InstructionSet(instruction_list)
