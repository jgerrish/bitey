import pytest

from bitey.cpu.flag import Flag, Flags, FlagJSONDecoder, FlagsJSONDecoder


def test_cpu_flag_init():
    f = Flag("C", "Carry", 0)
    assert f.short_name == "C"
    assert f.name == "Carry"
    assert f.bit_field_pos == 0


def test_cpu_flags_init():
    f1 = Flag("C", "Carry", 0)
    f2 = Flag("Z", "Zero Result", 1)
    flags = Flags([f1, f2], 0)
    assert len(flags.flags) == 2
    assert type(flags.data) == int
    assert flags.data == 0
    assert flags["C"] == f1
    assert flags["Z"] == f2


def test_cpu_flags_json_decoder():
    f = open("chip/6502.json")
    s = f.read()
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 7
    # assert flags["A"] == Flag("A", 8)
    # assert flags["X"] == Flag("X", 8)
    # assert flags["Y"] == Flag("Y", 8)
