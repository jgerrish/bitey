from bitey.computer.computer import Computer
from bitey.cpu.cpu import CPU


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_cpu_instruction_rts():
    "Test loading a JSR instruction from memory, executing it and returnning with RTS"
    computer = build_computer()

    # Absolute mode JSR instruction
    computer.memory.write(0x00, 0x20)

    # Pointer to the address containing the address of the subroutine
    # (absolute addressing mode)
    computer.memory.write(0x01, 0x05)
    computer.memory.write(0x02, 0x00)

    # The next instruction that RTS returns to (NOP)
    computer.memory.write(0x03, 0xEA)

    # The subroutine, just a RTS
    computer.memory.write(0x05, 0x60)

    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.registers["PC"].set(0x00)

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # assert jsr.assembly_str(computer) == "JSR  $0004"

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x05

    # The stack should contain the old address
    assert computer.cpu.registers["S"].get() == 0xFF - 0x02
    assert computer.memory.read(CPU.stack_base + 0xFF) == 0x00
    assert computer.memory.read(CPU.stack_base + 0xFE) == 0x03

    # Executing the next instruction (RTS) should return to 0x03
    instruction = computer.cpu.get_next_instruction(computer.memory)
    assert instruction.short_str() == "RTS"

    computer.cpu.execute_instruction(computer.memory)

    # The stack should be empty now
    assert computer.cpu.registers["S"].get() == CPU.stack_size - 0x01

    # The PC should be back to the main program
    assert computer.cpu.registers["PC"].get() == 0x03
