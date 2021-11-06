import pytest

from bitey.cpu.register import (
    Register,
    Registers,
    RegistersJSONDecoder,
)


def test_cpu_register_init():
    r = Register("A", "Accumulator", 8)
    assert r.short_name == "A"
    assert r.name == "Accumulator"
    assert r.size == 8


def test_cpu_registers_init():
    r1 = Register("A", "Accumulator", 8)
    r2 = Register("X", "Index register X", 8)
    registers = Registers([r1, r2])
    assert len(registers.registers) == 2
    assert registers["A"] == r1
    assert registers["X"] == r2


def test_cpu_registers_json_decoder():
    f = open("chip/6502.json")
    s = f.read()
    r = RegistersJSONDecoder()
    registers = r.decode(s)
    assert len(registers.registers) == 6
    assert registers["A"] == Register("A", "Accumulator", 8)
    assert registers["P"] == Register("P", "Processor Status Register", 8)
    assert registers["PC"] == Register("PC", "Program Counter", 16)
    assert registers["S"] == Register("S", "Stack pointer", 9)
    assert registers["X"] == Register("X", "Index register X", 8)
    assert registers["Y"] == Register("Y", "Index register Y", 8)
