from dataclasses import dataclass
import json
from json import JSONDecoder
from typing import ClassVar

from bitey.cpu.flag.flag import Flag, Flags
from bitey.cpu.flag.zero_flag import ZeroFlag


@dataclass
class FlagJSONDecoder(JSONDecoder):
    flag_map: ClassVar[dict[str, Flag]] = {
        "Z": ZeroFlag,
    }

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

            short_name = json_doc["short_name"]

            # Create a specific class if it exists
            if short_name in FlagJSONDecoder.flag_map:
                flag_class = FlagJSONDecoder.flag_map[short_name]
                return flag_class(
                    short_name,
                    json_doc["name"],
                    json_doc["bit_field_pos"],
                    status,
                )

            return Flag(
                short_name,
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
        # TODO: Some things should be initialized to certain values
        # Make sure setting the flags byte to zero on start is ok
        return Flags(flag_list, None)