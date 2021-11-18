from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    ImmediateAddressingMode,
    ImpliedAddressingMode,
    ZeroPageAddressingMode,
)
from bitey.computer.computer import Computer
from bitey.memory.memory import Memory

def build_computer():
    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        assert len(computer.memory.memory) == 65536
        return computer
    return None

def test_cpu_addressing_mode_implied_addressing_mode():
    iam = ImpliedAddressingMode()
    assert type(iam) == ImpliedAddressingMode
    assert iam.get_value(None, None, None) is None

def test_cpu_addressing_mode_absolute_addressing_mode():
    computer = build_computer()
    computer.memory.write(11, 0x10)
    computer.memory.write(12, 0x20)
    computer.memory.write(0x2010, 0x33)

    computer.cpu.registers["PC"].value = 11
    
    aam = AbsoluteAddressingMode()
    assert type(aam) == AbsoluteAddressingMode

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert aam.adl == 0x10
    assert aam.adh == 0x20

    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 13

def test_cpu_addressing_mode_immediate_addressing_mode():
    computer = build_computer()
    computer.memory.write(11, 0x10)
    computer.memory.write(12, 0x20)

    computer.cpu.registers["PC"].value = 11
    
    iam = ImmediateAddressingMode()
    assert type(iam) == ImmediateAddressingMode
    value = iam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0x10
    assert computer.cpu.registers["PC"].value == 12

def test_cpu_addressing_mode_zeropage_addressing_mode():
    computer = build_computer()
    computer.memory.write(11, 0x10)
    computer.memory.write(0x10, 0x33)
    
    computer.cpu.registers["PC"].value = 11
    
    zpam = ZeroPageAddressingMode()
    assert type(zpam) == ZeroPageAddressingMode

    value = zpam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 12
