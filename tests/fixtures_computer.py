from bitey.computer.computer import Computer
from bitey.cpu.instruction.instruction import IncompleteInstruction


def build_computer():
    "Build the computer"
    computer = None

    with open("chip/6502.json") as f:
        chip_data = f.read()
        computer = Computer.build_from_json(chip_data)
        return computer

    return None


def init_computer():
    "Initialize computer for tests"
    computer = build_computer()
    flags = computer.cpu.flags
    assert flags["Z"].status is False

    assert computer.cpu.registers["PC"].get() == 1
    computer.cpu.registers["PC"].set(0x00)

    return computer


def execute_instruction(
    computer,
    expected_z_flag,
    expected_n_flag,
    expected_c_flag,
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    # i1 = ROL("ROL", opcode, "Rotate One Bit Left (Memory or Accumulator)")
    computer.cpu.registers["PC"].set(0x00)

    try:
        computer.step()
        # i1.execute(computer.cpu, computer.memory)
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
        assert flags["Z"].status is expected_c_flag
    except IncompleteInstruction:
        assert False
