from dataclasses import dataclass
import json
from json import JSONDecoder

from bitey.cpu.addressing_mode import AddressingMode
from bitey.cpu.addressing_mode_factory import AddressingModeFactory


@dataclass
class Opcode:
    """
    A CPU instruction opcode
    This specifies the machine code for the instruction and the
    addressing mode
    """

    "The instruction opcode"
    opcode: str

    "The instruction addressing mode"
    addressing_mode: AddressingMode

    def execute(self, flags, registers, memory):
        "Execute the opcode"
        # TODO: Implement this
        # value = self.addressing_mode.get_value(flags, registers, memory)
        self.set_flags(flags, registers)

        return

    def set_flags(self, flags, registers):
        flags["Z"].test_register_result(registers["X"])
        return


@dataclass
class Opcodes:
    """
    A set of Opcodes
    """

    opcodes: list[Opcode]

    def __post_init__(self):
        "Create a dictionary so we can access opcodes by short name"
        self.opcode_dict = {}
        for opcode in self.opcodes:
            self.opcode_dict[opcode.opcode] = opcode

    def __iter__(self):
        return iter(self.opcodes)

    def __len__(self):
        return len(self.opcodes)

    def __contains__(self, key):
        return key in self.opcode_dict

    def __getitem__(self, i):
        return self.opcode_dict[i]


class OpcodeJSONDecoder(JSONDecoder):
    """
    Decode an opcode definition in JSON format
    """

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        if ("opcode" in parsed_json) and ("addressing_mode" in parsed_json):
            addressing_mode = AddressingModeFactory.build(
                parsed_json["addressing_mode"]
            )
            return Opcode(parsed_json["opcode"], addressing_mode)
        else:
            # Return None if the opcode JSON object is missing fields or invalid
            return None


class OpcodesJSONDecoder(JSONDecoder):
    """
    Decode a set of opcode definitions in JSON format
    """

    def decode(self, json_doc):
        j = json.loads(json_doc)
        return self.decode_parsed(j)

    def decode_parsed(self, parsed_json):
        opcode_list = []
        ojd = OpcodeJSONDecoder()
        for opcode in parsed_json:
            opcode = ojd.decode_parsed(opcode)
            # Only append the opcode if all fields are present and the JSON
            # is valid for the opcode
            if opcode:
                opcode_list.append(opcode)
        return Opcodes(opcode_list)
