from bitey.computer.computer import Computer


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_cpu_instruction_beq_zero_flag_false():
    "Test BEQ when zero flag is False"
    computer = build_computer()

    computer.cpu.registers["X"].set(0x02)
    computer.cpu.registers["PC"].set(0x00)

    # DEX
    computer.memory.write(0x00, 0xCA)
    # BEQ to relative address -2 (the DEX instruction)
    computer.memory.write(0x01, 0xF0)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["Z"].status is False

    # BEQ should continue to the next instruction
    assert computer.cpu.registers["PC"].get() == 0x03


def test_cpu_instruction_beq_zero_flag_true():
    "Test BEQ when zero flag is True"
    computer = build_computer()

    computer.cpu.registers["X"].set(0x01)
    computer.cpu.registers["PC"].set(0x00)

    # DEX
    computer.memory.write(0x00, 0xCA)
    # BEQ to relative address -2 (the DEX instruction)
    computer.memory.write(0x01, 0xF0)
    computer.memory.write(0x02, 0xFD)
    # NOP
    computer.memory.write(0x03, 0xEA)

    # Step through 2 instructions
    computer.cpu.step(computer.memory, 2)

    assert computer.cpu.flags["Z"].status is True

    # BEQ should jump
    assert computer.cpu.registers["PC"].get() == 0x00
