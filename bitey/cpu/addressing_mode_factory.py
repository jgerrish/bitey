from dataclasses import dataclass
from typing import ClassVar
from bitey.cpu.addressing_mode import (
    AddressingMode,
    AbsoluteAddressingMode,
    ImmediateAddressingMode,
    ImpliedAddressingMode,
    ZeroPageAddressingMode,
)


@dataclass
class AddressingModeFactory:
    addressing_mode_map: ClassVar[dict[str, AddressingMode]] = {
        "absolute": AbsoluteAddressingMode,
        "immediate": ImmediateAddressingMode,
        "implied": ImpliedAddressingMode,
        "zeropage": ZeroPageAddressingMode,
    }

    def build(addressing_mode):
        "Build an AddressingMode instance from a string"
        return AddressingModeFactory.get_mode_from_str(addressing_mode)()

    def get_mode_from_str(addressing_mode):
        "Given an addressing mode string, return the addressing mode class"
        m = AddressingModeFactory.addressing_mode_map[addressing_mode]

        return m
