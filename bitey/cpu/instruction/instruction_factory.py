from dataclasses import dataclass
from typing import ClassVar

from bitey.cpu.instruction.instruction import (
    Instruction,
    InstructionClass,
    UnimplementedInstruction,
)
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

    def build(name, opcode, description):
        """
        Build an Instruction instance
        This builds an instruction from an instruction name, opcode and description.
        The opcode is an Opcode class.
        """
        try:
            return InstructionFactory.get_instruction_from_opcode(opcode)(
                name, opcode, description
            )
        except UnimplementedInstruction:
            # Use the base class for the instruction
            return Instruction(name, opcode, description)

    def get_instruction_from_opcode(opcode):
        "Given an opcode class, return the instruction class"
        inst = None
        if opcode.opcode in InstructionFactory.instruction_map:
            inst = InstructionFactory.instruction_map[opcode.opcode]
        else:
            raise UnimplementedInstruction

        return inst


@dataclass
class InstructionClassFactory:
    instruction_map: ClassVar[dict[str, (InstructionClass, Instruction)]] = {
        0: BRK,
        88: CLI,
        120: SEI,
        141: STA,
        154: TXS,
        162: LDX,
        173: LDA,
        # 0: (InstructionClass, BRK),
        # 88: (InstructionClass, CLI),
        # 120: (InstructionClass, SEI),
        # 141: (InstructionClass, STA),
        # 154: (InstructionClass, TXS),
        # 162: (InstructionClass, LDX),
        # 173: (InstructionClass, LDA),
    }

    def build(name, opcodes, description):
        """
        Build an Instruction instance
        This builds an instruction from an instruction name,
        list of opcodes and description.
        TODO: Refactor this
        """
        # TODO: Refactor this
        if len(opcodes.opcodes) > 0:
            opcode = opcodes.opcodes[0].opcode
            try:
                inst = InstructionClassFactory.get_instruction_class_from_opcode(
                    opcode
                )(name, opcodes, description)
                return InstructionClass(name, inst, opcodes, description)
            except UnimplementedInstruction:
                # Use the base class for the instruction
                return InstructionClass(name, None, opcodes, description)
        else:
            return None

    def get_instruction_class_from_opcode(opcode):
        "Given an opcode string, return the instruction class"
        if opcode in InstructionFactory.instruction_map:
            inst = InstructionClassFactory.instruction_map[opcode]
        else:
            raise UnimplementedInstruction

        return inst
