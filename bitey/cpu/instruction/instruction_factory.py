from dataclasses import dataclass
from typing import ClassVar

from bitey.cpu.instruction.instruction import Instruction, UnimplementedInstruction
from bitey.cpu.instruction.brk import BRK
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.sei import SEI
from bitey.cpu.instruction.lda import LDA
from bitey.cpu.instruction.sta import STA
from bitey.cpu.instruction.txs import TXS
from bitey.cpu.instruction.ldx import LDX


@dataclass
class InstructionFactory:
    instruction_map: ClassVar[dict[str, Instruction]] = {
        0: BRK,
        88: CLI,
        120: SEI,
        141: STA,
        154: TXS,
        162: LDX,
        173: LDA,
    }

    def build(name, opcodes, description):
        "Build an Instruction instance"
        # TODO: Refactor this
        if len(opcodes.opcodes) > 0:
            opcode = opcodes.opcodes[0].opcode
            return InstructionFactory.get_instruction_from_opcode(opcode)(
                name, opcodes, description
            )
        else:
            return None

    def get_instruction_from_opcode(opcode):
        "Given an opcode string, return the instruction class"
        if opcode in InstructionFactory.instruction_map:
            inst = InstructionFactory.instruction_map[opcode]
        else:
            raise UnimplementedInstruction

        return inst
