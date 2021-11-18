from dataclasses import dataclass
from enum import Enum


class State(Enum):
    "State of a pin, can either be LOW or HIGH"
    LOW = 1
    HIGH = 2

@dataclass
class Pin:
    """
    Physical pins on the microprocessor.
    Most of the code in this project is higher-level, ignoring
    things like clock-cycles and physical structure of the address
    and data bus.

    The Pin and Pins classes provide some exceptions to this general rule.

    In particular, the reset pin provides a safe start to the initialization
    of the processor.
    """

    "Name of the pin"
    name: str = ""

    "Short name of the pin"
    short_name: str = ""

    """
    State of the pin, low or high
    Default to low, so the processor is in reset mode.
    Some other pins may need to be broght high to be in a normal state,
    such as the IRQ pin.
    """
    state: State = State.LOW


    def set_high(self):
        self.state = State.HIGH

    def set_low(self):
        self.state = State.LOW

    def get(self):
        return self.state


@dataclass
class RST(Pin):
    """
    The reset pin
    When the reset pin is low, the processor is in an uninitialized state.
    """

class IRQ(Pin):
    """
    The IRQ pin
    When the IRQ line is low, an interrupt has been requested.
    Multiple lines may be connected to this pin.
    """
    
@dataclass
class Pins:
    """
    The set of pins on the CPU
    """
    pins: list[Pin]


    def __post_init__(self):
        "Create a dictionary so we can access pins by short name"
        self.pin_dict = {}
        for f in self.pins:
            self.pin_dict[f.short_name] = f

    def __getitem__(self, i):
        return self.pin_dict[i]
