from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.addressing_mode_factory import AddressingModeFactory


def test_cpu_addressing_mode_addressing_mode_map():
    am = AddressingModeFactory.get_mode_from_str("absolute")
    assert am == AbsoluteAddressingMode


def test_cpu_addressing_mode_build():
    am = AddressingModeFactory.build("absolute")
    assert am == AbsoluteAddressingMode()
