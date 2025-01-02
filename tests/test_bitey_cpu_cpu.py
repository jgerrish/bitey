from bitey.cpu.addressing_mode import AccumulatorAddressingMode, ImpliedAddressingMode
from bitey.cpu.cpu import (
    CPU,
    CPUBreakpoint,
    CPUState,
    CPUStateChange,
    CPUJSONDecoder,
    StackOverflow,
    StackUnderflow,
)
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

    assert len(cpu.flags.flags) == 8
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
    assert cpu.registers["S"].value == 0xFF


def test_cpu_cpu_stack_push():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)
    assert cpu.registers["S"].value == 0xFE
    assert memory.memory[0x01FF] == 3


def test_cpu_cpu_stack_push_stack_overflow():
    """
    Test for stack overflow.

    Current behavior has the stack wrapping on overflow.
    """
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.registers["S"].value = 0x00
    try:
        cpu.stack_push(memory, 3)
        assert memory.read(0x100) == 3
    except StackOverflow:
        assert False


def test_cpu_cpu_stack_push_stack_underflow():
    """
    Test for stack overflow.

    Current behavior has the stack wrapping on underflow.
    """
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    for x in range(65536):
        memory.memory[x] = x % 256

    cpu.stack_init()

    try:
        result = cpu.stack_pop(memory)
        assert result == 0x01
        assert cpu.registers["S"].value == 0x01
    except StackUnderflow:
        assert False


def test_cpu_cpu_stack_pop():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)

    value = cpu.stack_pop(memory)

    assert value == 3
    assert cpu.registers["S"].value == 0xFF


def test_cpu_cpu_stack_pull():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    cpu.stack_push(memory, 3)

    value = cpu.stack_pull(memory)

    assert value == 3
    assert cpu.registers["S"].value == 0xFF


def test_cpu_cpu_stack_push_address():
    cpu = build_cpu()
    memory = Memory(bytearray(65536))
    cpu.stack_init()

    address = 0x2010

    cpu.stack_push_address(memory, address)

    assert memory.read(0x01FF) == 0x20
    assert memory.read(0x01FE) == 0x10
    assert cpu.registers["S"].value == 0xFD


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


# Tests around changing processor state


def test_cpu_cpu_set_state_change():
    "Test that changing the processor state to a different state works"
    cpu = build_cpu()
    cpu.stack_init()

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        # The state should change and an exception should be raised
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING


def test_cpu_cpu_set_state_no_change():
    "Test that changing the processor state to the same state works"
    cpu = build_cpu()
    cpu.stack_init()

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.STOPPED)
    except CPUStateChange:
        # There should be no state change
        assert False
    else:
        assert True

    assert cpu.state == CPUState.STOPPED


# Tests around processor limits and auditing


# Test a processor instruction load limit of 0 instructions
def test_cpu_cpu_num_instructions_loaded_limit_0():
    """
    Test that setting a number of instructions loaded limit of zero fails
    if any instruction is loaded.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # One NOP instruction
    memory.write(0x00, 0xEA)

    cpu.num_instructions_loaded_limit = 0
    assert cpu.registers["PC"].value == 0x00

    # reset hasn't been called, so the number of instructions loaded is zero
    assert cpu.num_instructions_loaded == 0
    assert cpu.num_instructions_loaded_limit == 0

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange as e:
        # The state should change and an exception should be raised
        assert e.state == CPUState.STOPPED
        assert cpu.state == CPUState.STOPPED

    assert cpu.num_instructions_loaded == 0


# Test a processor instruction execute limit of 0 instructions
def test_cpu_cpu_num_instructions_execute_limit_0():
    """
    Test that setting a number of instructions execute limit of zero
    fails if any instruction is executed.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # One NOP instruction
    memory.write(0x00, 0xEA)

    cpu.num_instructions_executed_limit = 0
    assert cpu.registers["PC"].value == 0x00

    # reset hasn't been called, so the number of instructions executed is zero
    assert cpu.num_instructions_executed == 0
    assert cpu.num_instructions_executed_limit == 0

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    # Just loading the instruction should be fine
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        assert False

    # Trying to execute it should fail
    try:
        cpu.execute_instruction(memory)
    except CPUStateChange as e:
        # The state should change and an exception should be raised
        assert e.state == CPUState.STOPPED
        assert cpu.state == CPUState.STOPPED

    assert cpu.num_instructions_executed == 0


# Test a processor instruction load limit of 1 instructions
def test_cpu_cpu_num_instructions_loaded_limit_1():
    """
    Test that setting a number of instructions loaded limit of one fails
    if any instruction is loaded.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Two NOP instructions
    memory.write(0x00, 0xEA)
    memory.write(0x01, 0xEA)

    cpu.num_instructions_loaded_limit = 1
    assert cpu.registers["PC"].value == 0x00

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_loaded == 1

    assert cpu.state == CPUState.RUNNING
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange as e:
        # The state should have changed
        assert e.state == CPUState.STOPPED
    else:
        assert False

    assert cpu.num_instructions_loaded == 1


# Test a processor instruction execute limit of 1 instructions
def test_cpu_cpu_num_instructions_executed_limit_1():  # noqa: C901
    """
    Test that setting a number of instructions executed limit of one fails
    if any instruction is executed.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Two NOP instructions
    memory.write(0x00, 0xEA)
    memory.write(0x01, 0xEA)

    cpu.num_instructions_executed_limit = 1
    assert cpu.registers["PC"].value == 0x00

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    # Just loading the instruction should be fine
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    # Trying to execute it should also work
    try:
        cpu.execute_instruction(memory)
    except CPUStateChange:
        # The state should change and an exception should be raised
        assert False

    assert cpu.num_instructions_executed == 1

    assert cpu.state == CPUState.RUNNING

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_loaded == 2

    try:
        cpu.execute_instruction(memory)
    except CPUStateChange as e:
        # The state should change and an exception should be raised
        assert e.state == CPUState.STOPPED
    else:
        assert False

    assert cpu.num_instructions_executed == 1


# Test a processor instruction load limit of 2 instructions
def test_cpu_cpu_num_instructions_loaded_limit_2():
    """
    Test that setting a number of instructions loaded limit of two instructions passes
    if any instruction is loaded.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Three NOP instructions
    memory.write(0x01, 0xEA)
    memory.write(0x02, 0xEA)
    memory.write(0x03, 0xEA)

    cpu.num_instructions_loaded_limit = 2
    assert cpu.registers["PC"].value == 0x00

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_loaded == 1

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_loaded == 2

    assert cpu.state == CPUState.RUNNING
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange as e:
        # The state should have changed
        assert e.state == CPUState.STOPPED
    else:
        assert False

    assert cpu.num_instructions_loaded == 2


# Test a processor instruction execute limit of 2 instructions
# Test a processor instruction load limit of 2 instructions
def test_cpu_cpu_num_instructions_executed_limit_2():  # noqa: C901
    """
    Test that setting a number of instructions executed limit of two instructions passes
    if any instruction is executed.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Three NOP instructions
    memory.write(0x01, 0xEA)
    memory.write(0x02, 0xEA)
    memory.write(0x03, 0xEA)

    cpu.num_instructions_executed_limit = 2
    assert cpu.registers["PC"].value == 0x00

    assert cpu.state == CPUState.STOPPED

    try:
        cpu.set_state(CPUState.RUNNING)
    except CPUStateChange as e:
        assert e.state == CPUState.RUNNING
        assert cpu.state == CPUState.RUNNING

    # Just loading the instruction should be fine
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    # Trying to execute it should also work
    try:
        cpu.execute_instruction(memory)
    except CPUStateChange:
        # The state should change and an exception should be raised
        assert False

    assert cpu.num_instructions_executed == 1

    # Just loading the instruction should be fine
    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    # Trying to execute it should also work
    try:
        cpu.execute_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_executed == 2

    assert cpu.state == CPUState.RUNNING

    try:
        cpu.get_next_instruction(memory)
    except CPUStateChange:
        # The state should not change and an exception should not be raised
        assert False

    assert cpu.num_instructions_loaded == 3

    try:
        cpu.execute_instruction(memory)
    except CPUStateChange as e:
        # The state should change and an exception should be raised
        assert e.state == CPUState.STOPPED
    else:
        assert False

    assert cpu.num_instructions_executed == 2


# Tests around processor breakpoints and watchpoints


def test_cpu_cpu_set_breakpoint():
    """
    Test that setting a breakpoint triggers it on stepping.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Three NOP instructions
    memory.write(0x01, 0xEA)
    memory.write(0x02, 0xEA)
    memory.write(0x03, 0xEA)

    assert cpu.registers["PC"].value == 0x00

    cpu.set_breakpoint(0x00)

    # Trying to step one instruction should trigger the breakpoint
    try:
        cpu.step(memory)
    except CPUBreakpoint as e:
        # An exception should be raised
        assert e.address == 0x00
    else:
        assert False


def test_cpu_cpu_clear_breakpoint():
    """
    Test that clearing a breakpoint doesn't trigger it on stepping.
    """
    cpu = build_cpu()
    cpu.stack_init()

    memory = Memory(bytearray(65536))
    # Three NOP instructions
    memory.write(0x01, 0xEA)
    memory.write(0x02, 0xEA)
    memory.write(0x03, 0xEA)

    assert cpu.registers["PC"].value == 0x00

    cpu.set_breakpoint(0x00)
    cpu.clear_breakpoint(0x00)

    # Trying to step one instruction should not trigger the breakpoint
    try:
        cpu.step(memory)
    except CPUBreakpoint:
        assert False
    else:
        assert True
