import pytest

from bitey.cpu.addressing_mode import AbsoluteAddressingMode


def test_cpu_addressing_mode_absolute_addressing_mode():
    aam = AbsoluteAddressingMode(0x10, 0x20)
    assert type(aam) == AbsoluteAddressingMode
    assert aam.adl == 0x10
    assert aam.adh == 0x20
