from dataclasses import dataclass
import json
from json import JSONDecoder

from bitey.listener import Listener
from bitey.watcher import Watcher


class RegisterOverflowException(Exception):
    "The Register was incremented past its size"


# dataclass generates __init__, __repr__ and other special methods for PEP526
# defined member variables
# __init__ parameters are defined in order of member variable definition
@dataclass
class Register(Watcher):
    """
    Class to represent a register
    Register's subclass the Watcher class and send updates when their value changes
    """

    short_name: str
    "The short name of the register, for example A"

    name: str
    "The name of the register, for example Accumulator"

    size: int
    "The size of the register in bits"

    value: int = 0
    "The value of the register"

    def __post_init__(self):
        # Subclasses must explicitly call the base class __init__ method
        # __post_init__ is called after other initialization
        # We don't want to make Watcher a dataclass since users of Register
        # don't need to know about Watcher's data
        super().__init__()

        self.flags_listener = Listener()
        self.flags_listener.register_callback(self.update_register_data)

    def __str__(self):
        "Return a string representation of the register"
        return "{}: 0x{:>02X}".format(self.short_name, self.value)

    def name(self):
        "The name of the register"
        return self.name

    def size(self):
        "The size of the register in bits"
        return self.size

    def inc(self):
        """
        Increment the register.
        If it wraps, usually the Z flag is set.
        """
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        if (self.value + 1) >= (2 ** self.size):
            self.value = 0x00
            # raise RegisterOverflowException
        else:
            self.value += 1
        self.update()

    def dec(self):
        """
        Decrement the register.
        If it wraps, usually the Z flag is set.
        """
        # TODO: Maybe wrap the flag with bounds checking too, read expected
        # behavior
        if (self.value - 1) < 0:
            self.value = (2 ** self.size) - 1
            # raise RegisterOverflowException
        else:
            self.value -= 1
        self.update()

    def get(self):
        """
        Get the register's value
        This getter should be used as the only way to get a register's value
        """
        return self.value

    def set(self, value, update=True):
        """
        Set the register's value
        This setter should be used as the only way to change the register's value
        """
        self.value = value
        if update:
            self.update()

    def add(self, amt):
        "Add an amount to the register's value"
        if (self.value + amt) >= (2 ** self.size):
            raise Exception

        self.value += amt
        self.update()

    def __eq__(self, value):
        """
        Implment equality so we can compare this register's value
        to other integer values without directly accessing .value
        """
        return self.value == value

    def update_register_data(self, flag):
        """
        Update register data when the Flags data is updated
        This is used to keep the P register and flags in sync
        """
        if self.short_name == "P":
            self.set(flag.data, False)


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

    def __str__(self):
        "Return a string representation of the registers"
        return ", ".join([str(x) for x in self.registers])

    def __getitem__(self, i):
        return self.regs[i]

    def set_logger(self, logger):
        self.logger = logger
        for register in self.registers:
            register.logger = logger


class RegisterJSONDecoder(JSONDecoder):
    """
    Decode a register definition in JSON format
    """

    def decode(self, json_doc):
        if (
            ("short_name" in json_doc)
            and ("name" in json_doc)
            and ("size" in json_doc)
            and ("value" in json_doc)
        ):
            return (
                Register(
                    json_doc["short_name"],
                    json_doc["name"],
                    json_doc["size"],
                    json_doc["value"],
                ),
            )
        elif (
            ("short_name" in json_doc) and ("name" in json_doc) and ("size" in json_doc)
        ):
            return Register(
                json_doc["short_name"], json_doc["name"], json_doc["size"], 0
            )
        else:
            return None


class RegistersJSONDecoder(JSONDecoder):
    """
    Decode a list of register definitions in JSON format
    """

    def decode(self, json_doc):
        parsed_json = json.loads(json_doc)
        return self.decode_parsed(parsed_json)

    def decode_parsed(self, parsed_json):
        register_list = []
        rjd = RegisterJSONDecoder()
        for register in parsed_json:
            r = rjd.decode(register)
            register_list.append(r)
        return Registers(register_list)
