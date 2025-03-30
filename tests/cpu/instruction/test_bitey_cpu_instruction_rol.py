import pytest
import tests.computer.computer
import tests.memory.memory

# TODO Maybe refactor so these are not needed
from bitey.cpu.addressing_mode import AccumulatorAddressingMode
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.instruction.opcode import Opcode
from bitey.cpu.instruction.rol import ROL


# module scope means run once per test module
@pytest.fixture(scope="module")
def setup():
    computer = tests.computer.computer.init_computer()
    yield computer


def execute_instruction(
    computer, opcode, expected_a_register, expected_z_flag, expected_n_flag
):
    "Execute the instruction based on an opcode"
    flags = computer.cpu.flags
    i1 = ROL("ROL", opcode, "Rotate One Bit Left (Memory or Accumulator)")

    try:
        i1.execute(computer.cpu, computer.memory)
        assert computer.cpu.registers["A"].get() == expected_a_register
        assert flags["Z"].status is expected_z_flag
        assert flags["N"].status is expected_n_flag
    except IncompleteInstruction:
        assert False


def test_cpu_instruction_rol_no_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b00101100)

    i1_opcode = Opcode(0x49, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01011000, False, False)


def test_cpu_instruction_rol_carry(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.flags["C"].set()
    computer.cpu.registers["A"].set(0b00101100)

    i1_opcode = Opcode(0x49, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01011001, False, False)


def test_cpu_instruction_rol_carry_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    assert computer.cpu.flags["C"].status is False
    computer.cpu.registers["A"].set(0b10101100)

    i1_opcode = Opcode(0x49, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b01011000, False, False)
    assert computer.cpu.flags["C"].status is True


def test_cpu_instruction_rol_negative_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["A"].set(0b01101100)

    i1_opcode = Opcode(0x49, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b11011000, False, True)


def test_cpu_instruction_rol_zero_set(setup):
    computer = setup
    computer.reset()

    computer.cpu.registers["PC"].set(0x00)
    computer.cpu.registers["A"].set(0b10000000)

    i1_opcode = Opcode(0x49, AccumulatorAddressingMode())
    execute_instruction(computer, i1_opcode, 0b00000000, True, False)


def test_cpu_instruction_rol_zeropage_no_carry(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x26), (0x01, 0x02), (0x02, 0b00101100)]
    )

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b01011000)], False, False, False
    )


def test_cpu_instruction_rol_zeropage_carry(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x26), (0x01, 0x02), (0x02, 0b00101100)]
    )

    computer.cpu.flags["C"].set()
    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b01011001)], False, False, False
    )


def test_cpu_instruction_rol_zeropage_carry_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x26), (0x01, 0x02), (0x02, 0b10101100)]
    )

    assert computer.cpu.flags["C"].status is False
    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b01011000)], False, False, True
    )


def test_cpu_instruction_rol_zeropage_negative_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x26), (0x01, 0x02), (0x02, 0b01101100)]
    )

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b11011000)], False, True, False
    )


def test_cpu_instruction_rol_zeropage_zero_set(setup):
    computer = setup
    computer.reset()

    tests.memory.memory.init_memory(
        computer.memory, [(0x00, 0x26), (0x01, 0x02), (0x02, 0b10000000)]
    )

    tests.computer.computer.execute_instruction(
        computer, [(0x02, 0b00000000)], True, False, True
    )
