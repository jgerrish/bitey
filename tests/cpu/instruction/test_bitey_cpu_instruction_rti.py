from bitey.computer.computer import Computer


def build_computer():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def test_build_cpu_instruction_rti():
    "Test the RTI instruction"
    computer = build_computer()

    # BRK instructions
    computer.memory.write(0x00, 0x00)
    computer.memory.write(0x01, 0xEA)
    # The interrupt vector pointer
    computer.memory.write(0xFFFE, 0x10)
    computer.memory.write(0xFFFF, 0x20)

    # Write a RTI instruction
    computer.memory.write(0x2010, 0x40)

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.registers["PC"].get() == 0x00

    computer.cpu.get_next_instruction(computer.memory)
    assert computer.cpu.registers["PC"].get() == 0x01
    computer.cpu.execute_instruction(computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x2010
    # Stack should be down three (two bytes for address, one for
    # process status register)
    assert computer.cpu.registers["S"] == 0x01FF - 0x003

    assert computer.memory.read(0x1FF) == 0x00
    assert computer.memory.read(0x1FE) == 0x01
    assert computer.memory.read(0x1FD) == 0b00010000

    computer.cpu.registers["P"].set(0xFF)
    assert computer.cpu.registers["P"].get() == 0xFF

    # Execute the return from interrupt instruction
    computer.cpu.step(computer.memory)

    # The PC should now be 0x05
    assert computer.cpu.registers["PC"].get() == 0x0001
    # Stack should be down three (two bytes for address, one for
    # process status register)
    assert computer.cpu.registers["S"].get() == 0x01FF

    assert computer.cpu.registers["P"].get() == 0b00010000
