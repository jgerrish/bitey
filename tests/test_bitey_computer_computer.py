from bitey.computer.computer import Computer
from bitey.memory.memory import Memory
import json


def test_computer_computer_init():
    with open("chip/6502.json") as f:
        chip_data = f.read()

        computer = Computer.build_from_json(chip_data)

        assert len(computer.memory.memory) == 65536


def test_computer_computer_load():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()

        computer = Computer.build_from_json(chip_data)

        assert len(computer.memory.memory) == 65536
    with open("data/test-code.json") as f:
        assert len(computer.memory.memory) == 65536
        memory_data_json = f.read()
        memory_data = json.loads(memory_data_json)

        computer.load(memory_data["memory"], 0xFFFC)

        assert computer.memory.memory[0xFFFB] == 0
        assert computer.memory.memory[0xFFFC] == memory_data["memory"][0]
        assert computer.memory.memory[0xFFFD] == memory_data["memory"][1]
        assert computer.memory.memory[0xFFFE] == 0


def test_computer_computer_run():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()

        computer = Computer.build_from_json(chip_data)

        assert len(computer.memory.memory) == 65536

    with open("data/test-code.json") as f:
        memory_data_json = f.read()
        memory_data = json.loads(memory_data_json)

        computer.load(memory_data["memory"], 0xFFFC)


def test_computer_computer_disassemble():
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()

        computer = Computer.build_from_json(chip_data)

        assert len(computer.memory.memory) == 65536

    computer.memory = Memory(bytearray(1))
    computer.memory.write(0x00, 0x18)

    assert computer.disassemble() == "0000  18        CLC"
