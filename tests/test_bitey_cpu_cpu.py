from bitey.cpu.addressing_mode import AccumulatorAddressingMode, ImpliedAddressingMode
from bitey.cpu.cpu import CPU, CPUJSONDecoder, StackOverflow, StackUnderflow
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.opcode import Opcode
from bitey.memory.memory import Memory


def build_cpu():
    f = open("chip/6502.json")
    chip_data = f.read()

    cpu = CPU.build_from_json(chip_data)

    return cpu


def test_cpu_builder():
    f = open("chip/6502.json")
    s = f.read()
    cpu_decoder = CPUJSONDecoder()
    cpu = cpu_decoder.decode(s)
    assert len(cpu.instruction_set.instructions) == 56

    inst = cpu.instruction_set.instructions[2]
    assert inst.name == "ASL"
    assert inst.opcodes.opcodes[0].opcode == 10
    assert inst.opcodes.opcodes[0].addressing_mode == AccumulatorAddressingMode()
    assert inst.description == "Shift Left One Bit (Memory or Accumulator)"


def test_cpu_cpu_init():
    cpu = build_cpu()

    assert len(cpu.flags.flags) == 7
    assert len(cpu.registers.registers) == 6
    assert len(cpu.instruction_set.instructions) == 56


def test_cpu_cpu_decode_instruction():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    assert cpu.registers["PC"].value == 0x00
    # CLI
    memory.write(0, 0x58)
    instruction = cpu.get_next_instruction(memory)
    opcode = Opcode(0x58, ImpliedAddressingMode())
    expected_instruction = CLI("CLI", opcode, "Clear Interrupt Disable Bit", None)
    assert instruction == expected_instruction


def test_cpu_cpu_stack_init():
    cpu = build_cpu()
    cpu.stack_init()
    assert cpu.registers["S"].value == 0x01FF


def test_cpu_cpu_stack_push():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)
    assert cpu.registers["S"].value == 0x01FE
    assert memory.memory[0x01FF] == 3


def test_cpu_cpu_stack_push_stack_overflow():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.registers["S"].value = 0x01FF - 0x0100
    try:
        cpu.stack_push(memory, 3)
        assert False
    except StackOverflow:
        assert True


def test_cpu_cpu_stack_push_stack_underflow():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    try:
        cpu.stack_pop(memory)
        assert False
    except StackUnderflow:
        assert True


def test_cpu_cpu_stack_pop():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)

    value = cpu.stack_pop(memory)

    assert value == 3
    assert cpu.registers["S"].value == 0x01FF


def test_cpu_cpu_stack_pull():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)

    value = cpu.stack_pull(memory)

    assert value == 3
    assert cpu.registers["S"].value == 0x01FF


def test_cpu_cpu_stack_push_address():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    address = 0x2010

    cpu.stack_push_address(memory, address)

    assert memory.read(0x01FF) == 0x20
    assert memory.read(0x01FE) == 0x10
    assert cpu.registers["S"].value == 0x01FD


def test_cpu_cpu_stack_pop_address():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    address = 0x2010

    cpu.stack_push_address(memory, address)

    address = cpu.stack_pop_address(memory)

    assert address == 0x2010


def test_cpu_cpu_step_one():
    "Test stepping through one instruction"
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    # Two LDX instructions
    memory.write(0x00, 0xE8)
    memory.write(0x01, 0xE8)

    cpu.registers["PC"].set(0x00)
    cpu.registers["X"].set(0x00)

    cpu.step(memory)

    assert cpu.registers["PC"].get() == 0x01
    assert cpu.current_instruction.short_str() == "INX"
    assert cpu.registers["X"].get() == 0x01


def test_cpu_cpu_step_two():
    "Test stepping through two instructions"
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    # Three LDX instructions
    memory.write(0x00, 0xE8)
    memory.write(0x01, 0xE8)
    memory.write(0x02, 0xE8)

    cpu.registers["PC"].set(0x00)
    cpu.registers["X"].set(0x00)

    cpu.step(memory, 2)

    assert cpu.registers["PC"].get() == 0x02
    assert cpu.current_instruction.short_str() == "INX"
    assert cpu.registers["X"].get() == 0x02


def test_cpu_cpu_p_register_set_updates_flags():
    "Test that updating the P register updates the flags bitvector"
    cpu = build_cpu()
    cpu.stack_init()

    assert cpu.registers["P"].get() == 0x00
    assert cpu.flags.data == 0
    assert not cpu.flags["C"].status
    assert not cpu.flags["Z"].status

    cpu.registers["P"].set(0x01)
    assert cpu.registers["P"].get() == 0x01
    assert cpu.flags.data == 0x01
    assert cpu.flags["C"].status
    assert not cpu.flags["Z"].status


def test_cpu_cpu_flags_set_updates_p_register():
    "Test that updating any of the flags updates the P register"
    cpu = build_cpu()
    cpu.stack_init()

    assert cpu.registers["P"].get() == 0x00
    assert cpu.flags.data == 0
    assert not cpu.flags["C"].status
    assert not cpu.flags["Z"].status

    # Setting the C flag should update the Processor Status register
    cpu.flags["C"].set()
    assert cpu.flags["C"].status
    assert not cpu.flags["Z"].status
    assert cpu.flags.data == 0x01
    assert cpu.registers["P"].get() == 0x01
