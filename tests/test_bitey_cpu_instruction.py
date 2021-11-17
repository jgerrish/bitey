from bitey.cpu.addressing_mode import (
    AbsoluteAddressingMode,
)

from bitey.cpu.instruction.instruction import (
    Instruction,
    Instructions,
)


def test_cpu_instruction_init():
    i = Instruction(
        "LDA", 173, AbsoluteAddressingMode(), "Load Accumulator with Memory"
    )
    assert i.name == "LDA"
    assert i.opcode == 173
    assert i.addressing_mode == AbsoluteAddressingMode()
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instruction_init_no_type_checking():
    "We're not doing strict type checking yet, so this should pass"
    i = Instruction("LDA", 173, "absolute", "Load Accumulator with Memory")
    assert i.name == "LDA"
    assert i.opcode == 173
    assert i.addressing_mode == "absolute"
    assert i.description == "Load Accumulator with Memory"


def test_cpu_instructions_init():
    i1 = Instruction("LDA", 173, "absolute", "Load Accumulator with Memory")
    i2 = Instruction("STA", 141, "absolute", "Store Accumulator in Memory")
    instructions = Instructions([i1, i2])
    assert len(instructions.instructions) == 2
    print(instructions.instructions)
    lda = instructions.get_by_opcode(173)
    assert lda == i1
