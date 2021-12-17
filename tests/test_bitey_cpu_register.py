import logging
from bitey.logger import setup_logger

from bitey.cpu.register import (
    RegisterOverflowException,
    Register,
    Registers,
    RegistersJSONDecoder,
)


def test_cpu_register_init():
    r = Register("A", "Accumulator", 8, 0)
    assert r.short_name == "A"
    assert r.name == "Accumulator"
    assert r.size == 8
    assert r.value == 0


def test_cpu_register_eq():
    r = Register("A", "Accumulator", 8, 0)
    assert r == 0

    r = Register("A", "Accumulator", 8, 7)
    assert r == 7


def test_cpu_registers_init():
    r1 = Register("A", "Accumulator", 8, 0)
    r2 = Register("X", "Index register X", 8, 0)
    registers = Registers([r1, r2])
    assert len(registers.registers) == 2
    assert registers["A"] == r1
    assert registers["X"] == r2


def test_cpu_register_pc_inc():
    setup_logger()
    r = Register("PC", "Program Counter", 16, 0)
    r.logger = logging.getLogger("bitey")
    assert r.value == 0
    r.inc()
    assert r.value == 1


def test_cpu_register_pc_no_exception_on_8bit_inc():
    setup_logger()
    r = Register("PC", "Program Counter", 16, 0xFF)
    r.logger = logging.getLogger("bitey")

    assert r.value == 0xFF
    try:
        r.inc()
        assert True
        assert r.value == 0x0100
    except RegisterOverflowException:
        assert False
        assert r.value == 0xFF


def test_cpu_register_pc_throws_exception_on_16bit_inc_overflow():
    setup_logger()
    r = Register("PC", "Program Counter", 16, 0xFFFF)
    r.logger = logging.getLogger("bitey")

    assert r.value == 0xFFFF
    try:
        r.inc()
        assert False
    except RegisterOverflowException:
        assert True
        assert r.value == 0xFFFF


def test_cpu_registers_json_decoder():
    s = """
    [
    {
        "short_name": "A",
        "name": "Accumulator",
        "size": 8
    },
    {
        "short_name": "P",
        "name": "Processor Status Register",
        "size": 8
    },
    {
        "short_name": "PC",
        "name": "Program Counter",
        "size": 16
    },
    {
        "short_name": "S",
        "name": "Stack pointer",
        "size": 9
    },
    {
        "short_name": "X",
        "name": "Index register X",
        "size": 8
    },
    {
        "short_name": "Y",
        "name": "Index register Y",
        "size": 8
    }
    ]
    """
    r = RegistersJSONDecoder()
    registers = r.decode(s)
    assert len(registers.registers) == 6
    assert registers["A"] == Register("A", "Accumulator", 8, 0)
    assert registers["P"] == Register("P", "Processor Status Register", 8, 0)
    assert registers["PC"] == Register("PC", "Program Counter", 16, 0)
    assert registers["S"] == Register("S", "Stack pointer", 9, 0)
    assert registers["X"] == Register("X", "Index register X", 8, 0)
    assert registers["Y"] == Register("Y", "Index register Y", 8, 0)
