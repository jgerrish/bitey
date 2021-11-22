from dataclasses import dataclass
from typing import ClassVar
from bitey.cpu.addressing_mode import (
    AddressingMode,
    AbsoluteAddressingMode,
    AbsoluteIndirectAddressingMode,
    AbsoluteXAddressingMode,
    AbsoluteYAddressingMode,
    AccumulatorAddressingMode,
    ImmediateAddressingMode,
    ImpliedAddressingMode,
    IndirectXAddressingMode,
    IndirectYAddressingMode,
    RelativeAddressingMode,
    ZeroPageAddressingMode,
    ZeroPageXAddressingMode,
    ZeroPageYAddressingMode,
)


@dataclass
class AddressingModeFactory:
    addressing_mode_map: ClassVar[dict[str, AddressingMode]] = {
        "absolute": AbsoluteAddressingMode,
        "absolute_indirect": AbsoluteIndirectAddressingMode,
        "absolute_x": AbsoluteXAddressingMode,
        "absolute_y": AbsoluteYAddressingMode,
        "accumulator": AccumulatorAddressingMode,
        "immediate": ImmediateAddressingMode,
        "implied": ImpliedAddressingMode,
        "indirect_x": IndirectXAddressingMode,
        "indirect_y": IndirectYAddressingMode,
        "relative": RelativeAddressingMode,
        "zeropage": ZeroPageAddressingMode,
        "zeropage_x": ZeroPageXAddressingMode,
        "zeropage_y": ZeroPageYAddressingMode,
    }

    def build(addressing_mode):
        "Build an AddressingMode instance from a string"
        return AddressingModeFactory.get_mode_from_str(addressing_mode)()

    def get_mode_from_str(addressing_mode):
        "Given an addressing mode string, return the addressing mode class"
        m = AddressingModeFactory.addressing_mode_map[addressing_mode]

        return m
