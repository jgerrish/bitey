from dataclasses import dataclass
import json
from json import JSONDecoder, JSONEncoder


# dataclass generates __init__, __repr__ and other special methods for PEP526
# defined member variables
# __init__ parameters are defined in order of member variable definition
@dataclass
class Register:
    """
    Base class to represent a register
    """

    "The short name of the register, for example A"
    short_name: str
    "The name of the register, for example Accumulator"
    name: str
    "The size of the register in bits"
    size: int

    def name(self):
        "The name of the register"
        return self.name

    def size(self):
        "The size of the register in bits"
        return self.size


@dataclass
class Registers:
    """
    Define a set of registers
    """

    registers: list[Register]

    def __post_init__(self):
        "Create a dictionary so we can access registers by name"
        self.regs = {}
        for r in self.registers:
            self.regs[r.short_name] = r

    def __getitem__(self, i):
        return self.regs[i]


class RegisterJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    """

    def decode(self, json_doc):
        if ("short_name" in json_doc) and ("name" in json_doc) and ("size" in json_doc):
            return Register(json_doc["short_name"], json_doc["name"], json_doc["size"])
        else:
            return None


class RegistersJSONDecoder(JSONDecoder):
    """
    Decode a list of register definitions in JSON format
    """

    def decode(self, json_doc):
        j = json.loads(json_doc)
        if "registers" in j:
            l = []
            rjd = RegisterJSONDecoder()
            for register in j["registers"]:
                r = rjd.decode(register)
                l.append(r)
            return Registers(l)
