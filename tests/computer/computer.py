from bitey.cpu.instruction.instruction import IncompleteInstruction
from bitey.computer.computer import Computer


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
    expected_memory,
    expected_z_flag,
    expected_n_flag,
    expected_c_flag,
):
    """
    Execute an instruction fetched from the PC and test memory and flags
    """
    flags = computer.cpu.flags
    computer.cpu.registers["PC"].set(0x00)

    try:
        computer.step()
        # Test that the memory is written correctly
        for mem in expected_memory:
            assert computer.memory.read(mem[0]) == mem[1]

        # Test the flags
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
        assert flags["C"].status is expected_c_flag
    except IncompleteInstruction:
        assert False


def execute_explicit_instruction(
    computer, opcode, instruction, expected_registers, expected_flags, expected_memory
):
    "Execute an explicit instruction based on an opcode"
    flags = computer.cpu.flags

    try:
        instruction.execute(computer.cpu, computer.memory)
        for register, value in expected_registers:
            assert computer.cpu.registers[register].get() == value
        for flag, value in expected_flags:
            assert flags[flag].status is value
        for address, value in expected_memory:
            assert computer.memory.read(address) == value
    except IncompleteInstruction:
        assert False
