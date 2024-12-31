import pytest

from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
    AbsoluteIndirectAddressingMode,
    AbsoluteIndirectPageBoundaryBugAddressingMode,
    AbsoluteXAddressingMode,
    AbsoluteYAddressingMode,
    AccumulatorAddressingMode,
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


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = build_computer()
    yield computer


def test_cpu_addressing_mode_implied_get_value():
    iam = ImpliedAddressingMode()
    assert isinstance(iam, ImpliedAddressingMode)
    assert iam.get_value(None, None, None) == (None, None)


def test_cpu_addressing_mode_absolute_get_value(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2010, 0x33)

    computer.cpu.registers["PC"].set(0x0B)

    aam = AbsoluteAddressingMode()
    assert isinstance(aam, AbsoluteAddressingMode)

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert aam.adl == 0x10
    assert aam.adh == 0x20

    assert value == (0x2010, 0x33)
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_indirect_get_value(setup):
    computer = setup
    computer.reset()

    # Pointer to the pointer to the effective address
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)

    # Pointer to the effective address
    computer.memory.write(0x2010, 0x33)
    computer.memory.write(0x2011, 0x55)

    computer.memory.write(0x5533, 0x11)

    computer.cpu.registers["PC"].set(0x0B)

    aam = AbsoluteIndirectAddressingMode()
    assert isinstance(aam, AbsoluteIndirectAddressingMode)

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    # adl and adh are the effective address low and high bytes
    # not the original address (PC + 1, PC + 2)
    assert aam.adl == 0x33
    assert aam.adh == 0x55

    assert value == (0x5533, 0x11)
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_immediate_get_value(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)

    computer.cpu.registers["PC"].set(0x0B)

    zpam = ZeroPageAddressingMode()
    assert isinstance(zpam, ZeroPageAddressingMode)

    value = zpam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert value == (0x10, 0x33)
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_zeropagex_get_value(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x51, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the X register
    computer.cpu.registers["X"].set(0x41)

    zpxam = ZeroPageXAddressingMode()
    assert isinstance(zpxam, ZeroPageXAddressingMode)

    (address, value) = zpxam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert address == 0x51
    assert value == 0xC1
    assert computer.cpu.registers["PC"].get() == 0x0C


def test_cpu_addressing_mode_zeropagex_get_value_wrap(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x05, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the X register
    computer.cpu.registers["X"].set(0xF5)

    zpxam = ZeroPageXAddressingMode()
    assert isinstance(zpxam, ZeroPageXAddressingMode)

    (address, value) = zpxam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0x05
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_zeropagex_get_value_wrap_on_255(setup):
    "Test wrapping exactly on a value of 0xFF"
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x06, 0xC1)
    computer.memory.write(0xFF, 0xFD)

    computer.cpu.registers["PC"].set(0x0B)

    # set the X register
    computer.cpu.registers["X"].set(0xEF)

    # The sum should be 0xFF

    zpxam = ZeroPageXAddressingMode()
    assert isinstance(zpxam, ZeroPageXAddressingMode)

    (address, value) = zpxam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert address == 0xFF
    assert value == 0xFD
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_zeropagey_get_value(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x51, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the Y register
    computer.cpu.registers["Y"].set(0x41)

    zpyam = ZeroPageYAddressingMode()
    assert isinstance(zpyam, ZeroPageYAddressingMode)

    (address, value) = zpyam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0x51
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_zeropagey_get_value_wrap(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0x05, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the Y register
    computer.cpu.registers["Y"].set(0xF5)

    zpyam = ZeroPageYAddressingMode()
    assert isinstance(zpyam, ZeroPageYAddressingMode)

    (address, value) = zpyam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0x05
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_zeropagey_get_value_nowrap_ff(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x10, 0x33)
    computer.memory.write(0xFF, 0xC1)

    computer.cpu.registers["PC"].set(0x0B)

    # set the Y register
    computer.cpu.registers["Y"].set(0xEF)

    zpyam = ZeroPageYAddressingMode()
    assert isinstance(zpyam, ZeroPageYAddressingMode)

    (address, value) = zpyam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0xFF
    assert value == 0xC1
    assert computer.cpu.registers["PC"].value == 0x0C


def test_cpu_addressing_mode_relative_get_value(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0xA0, 0x10)
    computer.memory.write(0x00B1, 0x12)

    computer.cpu.registers["PC"].set(0xA0)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0x00B1
    assert value == 0x12


def test_cpu_addressing_mode_relative_get_value_negative(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0070, 0xB0)
    computer.memory.write(0x0021, 0x1A)

    computer.cpu.registers["PC"].set(0x70)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0x0021
    assert value == 0x1A


def test_cpu_addressing_mode_relative_get_value_negative_lt_zero(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0020, 0xB0)
    computer.memory.write(0xFFD1, 0x15)

    computer.cpu.registers["PC"].set(0x20)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0xFFD1
    assert value == 0x15


def test_cpu_addressing_mode_relative_get_value_negative_page_crossing(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x70, 0xB0)
    computer.memory.write(0x0021, 0x08)

    computer.cpu.registers["PC"].set(0x70)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0x0021
    assert value == 0x08


def test_cpu_addressing_mode_relative_get_value_page_crossing(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0xA0, 0x60)
    computer.memory.write(0x0101, 0xD1)

    computer.cpu.registers["PC"].set(0xA0)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0x0101
    assert value == 0xD1


def test_cpu_addressing_mode_relative_get_value_gt_16_bit(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0xFFC0, 0x60)
    computer.memory.write(0x0021, 0x10)

    computer.cpu.registers["PC"].set(0xFFC0)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0x0021
    assert value == 0x0010


def test_cpu_addressing_mode_relative_get_value_lt_zero(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0003, 0x80)
    computer.memory.write(0xFF84, 0xF3)

    computer.cpu.registers["PC"].set(0x0003)

    rel = RelativeAddressingMode()
    assert isinstance(rel, RelativeAddressingMode)

    (addr, value) = rel.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert addr == 0xFF84
    assert value == 0xF3


def test_cpu_addressing_mode_indirect_indexed(setup):
    computer = setup
    computer.reset()

    # Zero Page ADL
    computer.memory.write(0x10, 0x70)
    # Zero Page ADH
    computer.memory.write(0x11, 0x0B)
    # Final address
    computer.memory.write(0x0B75, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["Y"].set(0x05)

    am = IndirectIndexedAddressingMode()
    assert isinstance(am, IndirectIndexedAddressingMode)

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0xB75, 0x73)


def test_cpu_addressing_mode_indirect_indexed_page_rollover(setup):
    computer = setup
    computer.reset()

    # Zero Page ADL
    computer.memory.write(0x10, 0x70)
    # Zero Page ADH
    computer.memory.write(0x11, 0xFF)
    # Final address
    computer.memory.write(0x0009, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["Y"].set(0x99)

    am = IndirectIndexedAddressingMode()
    assert isinstance(am, IndirectIndexedAddressingMode)

    (address, value) = am.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0x09

    assert value == 0x73


def test_cpu_addressing_mode_indirect_indexed_page_norollover_ffff(setup):
    computer = setup
    computer.reset()

    # Zero Page ADL
    computer.memory.write(0x10, 0x70)
    # Zero Page ADH
    computer.memory.write(0x11, 0xFF)
    # Final address
    computer.memory.write(0xFFFF, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["Y"].set(0x8F)

    am = IndirectIndexedAddressingMode()
    assert isinstance(am, IndirectIndexedAddressingMode)

    (address, value) = am.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert address == 0xFFFF

    assert value == 0x73


def test_cpu_addressing_mode_indexed_indirect(setup):
    computer = setup
    computer.reset()

    # Zero Page ADL
    computer.memory.write(0x14, 0x70)
    # Zero Page ADH
    computer.memory.write(0x15, 0x0B)
    # Final address
    computer.memory.write(0x0B70, 0x73)

    computer.cpu.registers["PC"].set(0x10)
    computer.cpu.registers["X"].set(0x04)

    am = IndexedIndirectAddressingMode()
    assert isinstance(am, IndexedIndirectAddressingMode)

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0x0B70, 0x73)


def test_cpu_addressing_mode_indexed_indirect_incorrect_wrap(setup):
    "Test for bug with incorrect wrap case"
    computer = setup
    computer.reset()

    # Zero Page ADL
    computer.memory.write(0xFF, 0x70)
    # Zero Page ADH
    computer.memory.write(0x00, 0x0B)
    # Final address
    computer.memory.write(0x0B70, 0x73)

    computer.cpu.registers["PC"].set(0xFB)
    computer.cpu.registers["X"].set(0x04)

    am = IndexedIndirectAddressingMode()
    assert isinstance(am, IndexedIndirectAddressingMode)

    value = am.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    assert value == (0x0B70, 0x73)


def test_cpu_addressing_mode_absolute_x(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2015, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0x05)

    axam = AbsoluteXAddressingMode()
    assert isinstance(axam, AbsoluteXAddressingMode)

    value = axam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert axam.adl == 0x10
    assert axam.adh == 0x20

    assert value == (0x2015, 0x33)
    assert computer.cpu.registers["PC"].value == 13


def test_cpu_addressing_mode_absolute_x_page_crossing(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2105, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0xF5)

    axam = AbsoluteXAddressingMode()
    assert isinstance(axam, AbsoluteXAddressingMode)

    value = axam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)
    assert axam.adl == 0x10
    assert axam.adh == 0x20

    assert value == (0x2105, 0x33)
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_x_eom_wrap(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0x0005, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0xF5)

    axam = AbsoluteXAddressingMode()
    assert isinstance(axam, AbsoluteXAddressingMode)

    (address, value) = axam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert axam.adl == 0x10
    assert axam.adh == 0xFF

    assert address == 0x05
    assert value == 0x33
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_x_eom_nowrap_ffff(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0x0006, 0x33)
    computer.memory.write(0xFFFF, 0xC4)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["X"].set(0xEF)

    axam = AbsoluteXAddressingMode()
    assert isinstance(axam, AbsoluteXAddressingMode)

    (address, value) = axam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert axam.adl == 0x10
    assert axam.adh == 0xFF

    assert address == 0xFFFF
    assert value == 0xC4
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_y(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2023, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0x13)

    ayam = AbsoluteYAddressingMode()
    assert isinstance(ayam, AbsoluteYAddressingMode)

    (address, value) = ayam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert ayam.adl == 0x10
    assert ayam.adh == 0x20

    assert value == 0x33
    assert address == 0x2023
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_y_page_crossing(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)
    computer.memory.write(0x2105, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0xF5)

    ayam = AbsoluteYAddressingMode()
    assert isinstance(ayam, AbsoluteYAddressingMode)

    (address, value) = ayam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert ayam.adl == 0x10
    assert ayam.adh == 0x20

    assert address == 0x2105
    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 0x0D


def test_cpu_addressing_mode_absolute_y_eom_wrap(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0x0005, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0xF5)

    ayam = AbsoluteYAddressingMode()
    assert isinstance(ayam, AbsoluteYAddressingMode)

    (address, value) = ayam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert ayam.adl == 0x10
    assert ayam.adh == 0xFF

    assert address == 0x0005
    assert value == 0x33
    assert computer.cpu.registers["PC"].value == 0x0D


def test_cpu_addressing_mode_absolute_y_eom_nowrap_ffff(setup):
    computer = setup
    computer.reset()

    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0xFF)
    computer.memory.write(0xFFFF, 0x33)

    computer.cpu.registers["PC"].set(0x0B)
    computer.cpu.registers["Y"].set(0xEF)

    ayam = AbsoluteYAddressingMode()
    assert isinstance(ayam, AbsoluteYAddressingMode)

    (address, value) = ayam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )
    assert ayam.adl == 0x10
    assert ayam.adh == 0xFF

    assert value == 0x33
    assert address == 0xFFFF
    assert computer.cpu.registers["PC"].value == 0x0D


def test_cpu_addressing_mode_absolute_indirect_get_instr_str(setup):
    computer = setup
    computer.reset()

    # Pointer to the address containing the effective address
    computer.memory.write(0x01, 0xA0)
    computer.memory.write(0x02, 0x00)

    # The pointer to the effective address
    computer.memory.write(0xA0, 0x05)
    computer.memory.write(0xA1, 0x00)

    computer.cpu.registers["PC"].set(0x01)

    aiam = AbsoluteIndirectAddressingMode()

    inst_str = aiam.get_inst_str(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert inst_str == "($0005)"


def test_cpu_addressing_mode_accumulator(setup):
    "Test accumulator addressing mode"
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0x13)

    aam = AccumulatorAddressingMode()

    inst_str = aam.get_inst_str(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert isinstance(aam, AccumulatorAddressingMode)

    (address, value) = aam.get_value(
        computer.cpu.flags, computer.cpu.registers, computer.memory
    )

    assert address is None
    assert value == 0x13
    assert computer.cpu.registers["PC"].get() == 0x00
    assert inst_str == ""


def test_cpu_addressing_mode_absolute_indirect_page_boundary_bug_get_value(setup):
    computer = setup
    computer.reset()

    # Pointer to the pointer to the effective address
    computer.memory.write(0x0B, 0x10)
    computer.memory.write(0x0C, 0x20)

    # Pointer to the effective address
    computer.memory.write(0x2010, 0x33)
    computer.memory.write(0x2011, 0x55)

    computer.memory.write(0x5533, 0x11)

    computer.cpu.registers["PC"].set(0x0B)

    aam = AbsoluteIndirectPageBoundaryBugAddressingMode(3)
    assert isinstance(aam, AbsoluteIndirectPageBoundaryBugAddressingMode)

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    # adl and adh are the effective address low and high bytes
    # not the original address (PC + 1, PC + 2)
    assert aam.adl == 0x33
    assert aam.adh == 0x55

    assert value == (0x5533, 0x11)
    assert computer.cpu.registers["PC"].get() == 0x0D


def test_cpu_addressing_mode_absolute_indirect_page_boundary_bug_wrap_get_value(setup):
    computer = setup
    computer.reset()

    # Pointer to the pointer to the effective address
    computer.memory.write(0x00FF, 0x10)
    computer.memory.write(0x0000, 0x20)

    # Pointer to the effective address
    computer.memory.write(0x2010, 0x33)
    computer.memory.write(0x2011, 0x55)

    computer.memory.write(0x5533, 0x11)

    computer.cpu.registers["PC"].set(0x00FF)

    aam = AbsoluteIndirectPageBoundaryBugAddressingMode(3)
    assert isinstance(aam, AbsoluteIndirectPageBoundaryBugAddressingMode)

    value = aam.get_value(computer.cpu.flags, computer.cpu.registers, computer.memory)

    # adl and adh are the effective address low and high bytes
    # not the original address (PC + 1, PC + 2)
    assert aam.adl == 0x33
    assert aam.adh == 0x55

    assert value == (0x5533, 0x11)

    # Technically, the JMP instruction is the only instruction that uses this "buggy"
    # mode, so this shouldn't matter
    assert computer.cpu.registers["PC"].get() == 0x101
