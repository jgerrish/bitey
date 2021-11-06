from dataclasses import dataclass
from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
)


@dataclass
class AddressingModeFactory:
    addressing_mode_map = {
        "absolute": AbsoluteAddressingMode,
    }

    def get_mode_from_str(self, s):
        "Given an addressing mode string, return the addressing mode class"
        m = self.addressing_mode_map[s]
        return m
