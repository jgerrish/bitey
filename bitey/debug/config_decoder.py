import json
from json import JSONDecoder
from bitey.debug.config import Config


class ConfigDecoder(JSONDecoder):
    """
    Decode a debugger configuration file in JSON format
    """

    def decode(self, json_doc):
        config_data = json.loads(json_doc)
        return self.decode_parsed(config_data)

    def decode_parsed(self, config_data):
        print("Found config_data")
        breakpoints = []
        watchpoints = []
        if "breakpoints" in config_data:
            for bp in config_data["breakpoints"]:
                new_bp = {}
                new_bp["description"] = bp["description"]
                if "address" in bp:
                    if type(bp["address"]) == str:
                        new_bp["address"] = int(bp["address"], 0)
                    elif type(bp["address"]) == int:
                        new_bp["address"] = bp["address"]
                    breakpoints.append(new_bp)
        if "watchpoints" in config_data:
            for wp in config_data["watchpoints"]:
                new_wp = {}
                new_wp["description"] = wp["description"]
                if "address" in wp:
                    if type(wp["address"]) == str:
                        new_wp["address"] = int(wp["address"], 0)
                    elif type(wp["address"]) == int:
                        new_wp["address"] = wp["address"]
                    watchpoints.append(new_wp)
        return Config(breakpoints, watchpoints)
