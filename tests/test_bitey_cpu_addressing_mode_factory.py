from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.addressing_mode_factory import AddressingModeFactory


def test_cpu_addressing_mode_addressing_mode_map():
    f = AddressingModeFactory()
    am = f.get_mode_from_str("absolute")
    assert am == AbsoluteAddressingMode
