import pytest
import re

from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.addressing_mode import AbsoluteIndirectAddressingMode

from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU

from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.jmp import JMP


def build_computer(chip_line=None):
    computer = None

    search = re.compile(".*[^a-zA-Z0-9_-].*")

    if (chip_line is not None) and (search.search(chip_line) is not None):
        raise Exception("Invalid chip_line, contains non-alphanumeric characters")

    fn = "chip/6502.json"
    if chip_line is not None:
        fn = "chip/{}-6502.json".format(chip_line)
    with open(fn) as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = build_computer()
    yield computer


def test_build_cpu_instruction_jmp_absolute(setup):
    "Test building an absolute JMP instruction and executing it"
    computer = setup
    computer.reset()

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0x05)
    computer.memory.write(0x02, 0x00)

    # The subroutine, just a NOP
    computer.memory.write(0x05, 0xEA)

    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.registers["PC"].set(0x01)

    opcode = Opcode(0x4C, AbsoluteAddressingMode())
    jmp = JMP("JMP", opcode, "Jump to New Location")

    jmp.execute(computer.cpu, computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack be unchanged
    assert computer.cpu.registers["S"].get() == CPU.stack_start


def test_cpu_instruction_jmp_absolute(setup):
    "Test loading an absolute JMP instruction from memory"
    computer = setup
    computer.reset()

    # Absolute mode JMP instruction
    computer.memory.write(0x00, 0x4C)

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0x05)
    computer.memory.write(0x02, 0x00)

    # The subroutine, just a NOP
    computer.memory.write(0x05, 0xEA)

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.registers["PC"].get() == 0x00

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack should contain the old address
    assert computer.cpu.registers["S"].get() == CPU.stack_start


def test_build_cpu_instruction_jmp_absolute_indirect(setup):
    "Test building an absolute indirect JMP instruction and executing it"
    computer = setup
    computer.reset()

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0xA0)
    computer.memory.write(0x02, 0x00)
    # The next instruction that RTS returns to
    computer.memory.write(0x03, 0x60)

    # The subroutine address
    computer.memory.write(0xA0, 0x05)
    computer.memory.write(0xA1, 0x00)

    # The subroutine, just a NOP
    computer.memory.write(0x05, 0xEA)

    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.registers["PC"].set(0x01)

    opcode = Opcode(0x6C, AbsoluteIndirectAddressingMode())
    jmp = JMP("JMP", opcode, "Jump to New Location")

    jmp.execute(computer.cpu, computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack be unchanged
    assert computer.cpu.registers["S"].get() == CPU.stack_start


def test_cpu_instruction_jmp_absolute_indirect(setup):
    "Test loading an absolute indirect JMP instruction from memory"
    computer = setup
    computer.reset()

    # Absolute mode JMP instruction
    computer.memory.write(0x00, 0x6C)

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0xA0)
    computer.memory.write(0x02, 0x00)
    # The next instruction that RTS returns to
    computer.memory.write(0x03, 0x60)

    # The subroutine address
    computer.memory.write(0xA0, 0x05)
    computer.memory.write(0xA1, 0x00)

    # The subroutine, just a NOP
    computer.memory.write(0x05, 0xEA)

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.registers["PC"].get() == 0x00

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack should contain the old address
    assert computer.cpu.registers["S"].get() == CPU.stack_start


def test_cpu_instruction_jmp_nmos_wrap():
    "Test buggy JMP instruction that wraps"
    computer = build_computer("nmos")
    computer.reset()

    computer.memory.write(0xFE, 0x6C)
    computer.memory.write(0x00, 0x9A)
    computer.memory.write(0xFF, 0x4D)
    computer.memory.write(0x9A4D, 0x4D)

    computer.cpu.registers["PC"].set(0x00FE, 0x45)

    computer.cpu.get_next_instruction(computer.memory)

    assert computer.cpu.current_instruction.opcode.opcode == 0x6C

    # Check this has a bug
    assert "page_boundary_bug" in computer.cpu.current_instruction.options
    assert computer.cpu.current_instruction.options["page_boundary_bug"]

    # execute the instruction
    computer.cpu.execute_instruction(computer.memory)

    # check that the address is correct
    assert computer.cpu.registers["PC"].get() == 0x004D


def test_cpu_instruction_jmp_nmos_nowrap():
    "Test buggy JMP instruction that doesn't wrap"
    computer = build_computer("nmos")
    computer.reset()

    computer.memory.write(0xFD, 0x6C)
    computer.memory.write(0xFE, 0x4D)
    computer.memory.write(0xFF, 0x9A)
    computer.memory.write(0x9A4D, 0x4D)

    computer.cpu.registers["PC"].set(0x00FD, 0x45)

    computer.cpu.get_next_instruction(computer.memory)

    assert computer.cpu.current_instruction.opcode.opcode == 0x6C

    # Check this has a bug
    assert "page_boundary_bug" in computer.cpu.current_instruction.options
    assert computer.cpu.current_instruction.options["page_boundary_bug"]

    # execute the instruction
    computer.cpu.execute_instruction(computer.memory)

    # check that the address is correct
    assert computer.cpu.registers["PC"].get() == 0x004D
