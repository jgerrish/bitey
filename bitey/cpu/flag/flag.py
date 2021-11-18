from dataclasses import dataclass
import json
from json import JSONDecoder


@dataclass
class Flag:
    """
    Processor flag or status register
    Examples can include the carry flag and overflow flag
    """

    """
    The short name of the flag
    Usually this is a single character such as C for the carry flag
    """
    short_name: str

    """
    The name of the flag
    For example, Carry for the carry flag
    """
    name: str

    "If the flag is stored in a bitfield, which bit position is it"
    bit_field_pos: int

    "Store the state of the register in a boolean flag"
    status: bool

    def set(self):
        "Set this flag.  Set it to true."
        self.status = True

    def clear(self):
        "Clear this flag.  Set it to False."
        self.status = False


@dataclass
class Flags:
    """
    Define a set of processor flags
    """

    flags: list[Flag]
    data: int

    def __post_init__(self):
        "Create a dictionary so we can access flags by short name"
        self.flag_dict = {}
        for f in self.flags:
            self.flag_dict[f.short_name] = f

    def __getitem__(self, i):
        return self.flag_dict[i]


class FlagJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    """

    def decode(self, json_doc):
        if (
            ("short_name" in json_doc)
            and ("name" in json_doc)
            and ("bit_field_pos" in json_doc)
            and ("status" in json_doc)
        ):
            status = False
            if json_doc["status"] == 0:
                status = False
            elif json_doc["status"] == 1:
                status = True

            return Flag(
                json_doc["short_name"],
                json_doc["name"],
                json_doc["bit_field_pos"],
                status,
            )
        else:
            # Return None if the flag JSON object is missing fields or invalid
            return None


class FlagsJSONDecoder(JSONDecoder):
    """
    Decode a list of register definitions in JSON format
    """

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        flag_list = []
        rjd = FlagJSONDecoder()
        for flag in parsed_json:
            f = rjd.decode(flag)
            # Only append the flag if all fields are present and the JSON
            # is valid for the flag
            if f:
                flag_list.append(f)
        return Flags(flag_list, None)
