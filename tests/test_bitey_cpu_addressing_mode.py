from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    AbsoluteXAddressingMode,
    AbsoluteYAddressingMode,
    ImmediateAddressingMode,
    ImpliedAddressingMode,
    IndexedIndirectAddressingMode,
    IndirectIndexedAddressingMode,
    ZeroPageAddressingMode,
    ZeroPageXAddressingMode,
    ZeroPageYAddressingMode,
    RelativeAddressingMode,
)
from bitey.computer.computer import Computer


def build_computer():
    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        assert len(computer.memory.memory) == 65536
        return computer
    return None


def test_cpu_addressing_mode_implied_get_value():
    iam = ImpliedAddressingMode()
    assert type(iam) == ImpliedAddressingMode
    assert iam.get_value(None, None, None) == (None, None)


def test_cpu_addressing_mode_absolute_get_value():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(12, 0x20)
    computer.memory.write(0x2010, 0x33)

    computer.cpu.registers["PC"].set(0x0B)

    aam = AbsoluteAddressingMode()
    assert type(aam) == AbsoluteAddressingMode

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert aam.adl == 0x10
    assert aam.adh == 0x20

    assert value == (0x2010, 0x33)
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_immediate_get_value():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(12, 0x20)

    computer.cpu.registers["PC"].set(0x0B)

    iam = ImmediateAddressingMode()
    assert type(iam) == ImmediateAddressingMode
    value = iam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == (None, 0x10)
    assert computer.cpu.registers["PC"].get() == 0x0C


def test_cpu_addressing_mode_zeropage_get_value():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)

    computer.cpu.registers["PC"].set(0x0B)

    zpam = ZeroPageAddressingMode()
    assert type(zpam) == ZeroPageAddressingMode

    value = zpam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == (0x10, 0x33)
    assert computer.cpu.registers["PC"].value == 12


def test_cpu_addressing_mode_zeropagex_get_value():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x51, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the X register
    computer.cpu.registers["X"].set(0x41)

    zpxam = ZeroPageXAddressingMode()
    assert type(zpxam) == ZeroPageXAddressingMode

    value = zpxam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0xC1
    assert computer.cpu.registers["PC"].get() == 0x0C


def test_cpu_addressing_mode_zeropagex_get_value_wrap():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x06, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the X register
    computer.cpu.registers["X"].set(0xF5)

    zpxam = ZeroPageXAddressingMode()
    assert type(zpxam) == ZeroPageXAddressingMode

    value = zpxam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 12


def test_cpu_addressing_mode_zeropagey_get_value():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x51, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the Y register
    computer.cpu.registers["Y"].set(0x41)

    zpyam = ZeroPageYAddressingMode()
    assert type(zpyam) == ZeroPageYAddressingMode

    value = zpyam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 12


def test_cpu_addressing_mode_zeropagey_get_value_wrap():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x06, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the Y register
    computer.cpu.registers["Y"].set(0xF5)

    zpyam = ZeroPageYAddressingMode()
    assert type(zpyam) == ZeroPageYAddressingMode

    value = zpyam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 12


def test_cpu_addressing_mode_relative_get_value():
    computer = build_computer()
    computer.memory.write(0xA0, 0x10)

    computer.cpu.registers["PC"].set(0xA0)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0xB1


def test_cpu_addressing_mode_relative_get_value_negative():
    computer = build_computer()
    computer.memory.write(0x70, 0xB0)

    computer.cpu.registers["PC"].set(0x70)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0x21


def test_cpu_addressing_mode_relative_get_value_negative_lt_zero():
    computer = build_computer()
    computer.memory.write(0x20, 0xB0)

    computer.cpu.registers["PC"].set(0x20)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0xFFD0


def test_cpu_addressing_mode_relative_get_value_negative_page_crossing():
    computer = build_computer()
    computer.memory.write(0x70, 0xB0)

    computer.cpu.registers["PC"].set(0x70)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0x21


def test_cpu_addressing_mode_relative_get_value_page_crossing():
    computer = build_computer()
    computer.memory.write(0xA0, 0x60)

    computer.cpu.registers["PC"].set(0xA0)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0x101


def test_cpu_addressing_mode_relative_get_value_gt_16_bit():
    computer = build_computer()
    computer.memory.write(0xFFC0, 0x60)

    computer.cpu.registers["PC"].set(0xFFC0)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0x0022


def test_cpu_addressing_mode_relative_get_value_lt_zero():
    computer = build_computer()
    computer.memory.write(0x0003, 0x80)

    computer.cpu.registers["PC"].set(0x0003)

    rel = RelativeAddressingMode()
    assert type(rel) == RelativeAddressingMode

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert value == 0xFF83


def test_cpu_addressing_mode_indirect_indexed():
    computer = build_computer()
    # Zero Page ADL
    computer.memory.write(0x10, 0x70)
    # Zero Page ADH
    computer.memory.write(0x11, 0x0B)
    # Final address
    computer.memory.write(0x0B75, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["Y"].set(0x05)

    am = IndirectIndexedAddressingMode()
    assert type(am) == IndirectIndexedAddressingMode

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0xB75, 0x73)


def test_cpu_addressing_mode_indirect_indexed_page_rollover():
    computer = build_computer()
    # Zero Page ADL
    computer.memory.write(0x10, 0x70)
    # Zero Page ADH
    computer.memory.write(0x11, 0xFF)
    # Final address
    computer.memory.write(0x000A, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["Y"].set(0x99)

    am = IndirectIndexedAddressingMode()
    assert type(am) == IndirectIndexedAddressingMode

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0x0A, 0x73)


def test_cpu_addressing_mode_indexed_indirect():
    computer = build_computer()
    # Zero Page ADL
    computer.memory.write(0x14, 0x70)
    # Zero Page ADH
    computer.memory.write(0x15, 0x0B)
    # Final address
    computer.memory.write(0x0B70, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["X"].set(0x04)

    am = IndexedIndirectAddressingMode()
    assert type(am) == IndexedIndirectAddressingMode

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0x0B70, 0x73)


def test_cpu_addressing_mode_absolute_x():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2015, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0x05)

    axam = AbsoluteXAddressingMode()
    assert type(axam) == AbsoluteXAddressingMode

    value = axam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert axam.adl == 0x10
    assert axam.adh == 0x20

    assert value == (0x2015, 0x33)
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_x_page_crossing():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2105, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0xF5)

    axam = AbsoluteXAddressingMode()
    assert type(axam) == AbsoluteXAddressingMode

    value = axam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert axam.adl == 0x10
    assert axam.adh == 0x20

    assert value == (0x2105, 0x33)
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_x_eom_wrap():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0x0006, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0xF5)

    axam = AbsoluteXAddressingMode()
    assert type(axam) == AbsoluteXAddressingMode

    value = axam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert axam.adl == 0x10
    assert axam.adh == 0xFF

    assert value == (0x06, 0x33)
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_y():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2023, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0x13)

    ayam = AbsoluteYAddressingMode()
    assert type(ayam) == AbsoluteYAddressingMode

    value = ayam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert ayam.adl == 0x10
    assert ayam.adh == 0x20

    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_y_page_crossing():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2105, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0xF5)

    ayam = AbsoluteYAddressingMode()
    assert type(ayam) == AbsoluteYAddressingMode

    value = ayam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert ayam.adl == 0x10
    assert ayam.adh == 0x20

    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_y_eom_wrap():
    computer = build_computer()
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0x0006, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0xF5)

    ayam = AbsoluteYAddressingMode()
    assert type(ayam) == AbsoluteYAddressingMode

    value = ayam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert ayam.adl == 0x10
    assert ayam.adh == 0xFF

    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 13
