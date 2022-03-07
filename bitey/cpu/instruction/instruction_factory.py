from dataclasses import dataclass
import logging
from typing import ClassVar

from bitey.cpu.instruction.instruction import (
    Instruction,
    InstructionClass,
    UnimplementedInstruction,
)
from bitey.cpu.instruction.beq import BEQ
from bitey.cpu.instruction.bne import BNE
from bitey.cpu.instruction.brk import BRK
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.dec import DEC
from bitey.cpu.instruction.dec import DEX
from bitey.cpu.instruction.dec import DEY
from bitey.cpu.instruction.inc import INC
from bitey.cpu.instruction.inc import INX
from bitey.cpu.instruction.inc import INY
from bitey.cpu.instruction.jsr import JSR
from bitey.cpu.instruction.nop import NOP
from bitey.cpu.instruction.sei import SEI
from bitey.cpu.instruction.lda import LDA
from bitey.cpu.instruction.sta import STA
from bitey.cpu.instruction.txs import TXS
from bitey.cpu.instruction.ldx import LDX
from bitey.cpu.instruction.rts import RTS


@dataclass
class InstructionFactory:
    instruction_map: ClassVar[dict[str, Instruction]] = {
        0: BRK,
        32: JSR,
        88: CLI,
        96: RTS,
        120: SEI,
        136: DEY,
        141: STA,
        154: TXS,
        162: LDX,
        173: LDA,
        198: DEC,
        200: INY,
        202: DEX,
        206: DEC,
        208: BNE,
        214: DEC,
        222: DEC,
        230: INC,
        232: INX,
        234: NOP,
        238: INC,
        240: BEQ,
        246: INC,
        254: INC,
    }

    def __post_init__(self):
        "Initialize the InstructionFactory"
        self.logger = logging.getLogger("bitey.cpu.instruction.instruction_factory")

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
            # self.logger.debug("UnimplementedInstruction, building Instruction instance")
            return Instruction(name, opcode, description)

    def get_instruction_from_opcode(opcode):
        "Given an opcode class, return the instruction class"
        inst = None
        if opcode.opcode in InstructionFactory.instruction_map:
            # self.logger.debug("building custom instance")
            inst = InstructionFactory.instruction_map[opcode.opcode]
        else:
            raise UnimplementedInstruction

        return inst


@dataclass
class InstructionClassFactory:
    instruction_map: ClassVar[dict[str, (InstructionClass, Instruction)]] = {
        0: BRK,
        32: JSR,
        88: CLI,
        96: RTS,
        120: SEI,
        136: DEY,
        141: STA,
        154: TXS,
        162: LDX,
        173: LDA,
        198: DEC,
        200: INY,
        202: DEX,
        206: DEC,
        208: BNE,
        214: DEC,
        222: DEC,
        230: INC,
        232: INX,
        234: NOP,
        238: INC,
        240: BEQ,
        246: INC,
        254: INC,
    }

    logger: ClassVar = logging.getLogger("bitey.cpu.instruction.instruction_factory")

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
        if opcode in InstructionClassFactory.instruction_map:
            inst = InstructionClassFactory.instruction_map[opcode]
            return inst
        else:
            raise UnimplementedInstruction
