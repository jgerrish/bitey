import pytest
from bitey.cpu.addressing_mode import AbsoluteAddressingMode

from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU

from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.jsr import JSR


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = build_computer()
    yield computer


def test_build_cpu_instruction_jsr(setup):
    "Test building an instruction and executing it"
    computer = setup
    computer.reset()

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0x05)
    computer.memory.write(0x02, 0x00)
    # The next instruction that RTS returns to
    computer.memory.write(0x03, 0x60)

    # The subroutine, just a RTS
    computer.memory.write(0x05, 0x69)

    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.registers["PC"].set(0x01)

    opcode = Opcode(0x20, AbsoluteAddressingMode())
    jsr = JSR("JSR", opcode, "Jump to New Location Saving Return Address")

    # assert jsr.assembly_str(computer) == "JSR  $0004"

    jsr.execute(computer.cpu, computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack should contain the old address
    assert computer.cpu.registers["S"].get() == CPU.stack_start - 0x02
    assert computer.memory.read(CPU.stack_start) == 0x00
    assert computer.memory.read(CPU.stack_start - 0x01) == 0x03


def test_cpu_instruction_jsr(setup):
    "Test loading a JSR instruction from memory"
    computer = setup
    computer.reset()

    # Absolute mode JSR instruction
    computer.memory.write(0x00, 0x20)

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0x05)
    computer.memory.write(0x02, 0x00)
    # The next instruction that RTS returns to
    computer.memory.write(0x03, 0x60)

    # The subroutine, just a RTS
    computer.memory.write(0x05, 0x69)

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.registers["PC"].get() == 0x00

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # assert jsr.assembly_str(computer) == "JSR  $0004"

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack should contain the old address
    assert computer.cpu.registers["S"].get() == CPU.stack_start - 0x02
    assert computer.memory.read(CPU.stack_start) == 0x00
    assert computer.memory.read(CPU.stack_start - 0x01) == 0x03
