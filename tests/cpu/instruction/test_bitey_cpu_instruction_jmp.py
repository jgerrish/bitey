from bitey.cpu.addressing_mode import AbsoluteAddressingMode
from bitey.cpu.addressing_mode import AbsoluteIndirectAddressingMode

from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU

from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.jmp import JMP


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_build_cpu_instruction_jmp_absolute():
    "Test building an absolute JMP instruction and executing it"
    computer = build_computer()

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


def test_cpu_instruction_jmp_absolute():
    "Test loading an absolute JMP instruction from memory"
    computer = build_computer()

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


def test_build_cpu_instruction_jmp_absolute_indirect():
    "Test building an absolute indirect JMP instruction and executing it"
    computer = build_computer()

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


def test_cpu_instruction_jmp_absolute_indirect():
    "Test loading an absolute indirect JMP instruction from memory"
    computer = build_computer()

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
