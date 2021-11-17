from dataclasses import dataclass
from typing import ClassVar
from bitey.cpu.instruction.instruction import Instruction

from bitey.cpu.instruction.lda import LDA
from bitey.cpu.instruction.sta import STA


@dataclass
class InstructionFactory:
    instruction_map: ClassVar[dict[str, Instruction]] = {
        141: STA,
        173: LDA,
    }

    def build(name, opcode, addressing_mode, description):
        "Build an Instruction instance from an opcode"
        return InstructionFactory.get_instruction_from_opcode(opcode)(
            name, opcode, addressing_mode, description
        )

    def get_instruction_from_opcode(opcode):
        "Given an addressing mode string, return the addressing mode class"
        inst = InstructionFactory.instruction_map[opcode]

        return inst
