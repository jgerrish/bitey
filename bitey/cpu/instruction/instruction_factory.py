from dataclasses import dataclass
import logging
from typing import ClassVar

from bitey.cpu.instruction.instruction import (
    Instruction,
    InstructionClass,
    UnimplementedInstruction,
)
from bitey.cpu.instruction.adc import ADC, ADCCMOS, ADCNMOS
from bitey.cpu.instruction.an import AND
from bitey.cpu.instruction.asl import ASL
from bitey.cpu.instruction.bcc import BCC
from bitey.cpu.instruction.bcs import BCS
from bitey.cpu.instruction.beq import BEQ
from bitey.cpu.instruction.bit import BIT
from bitey.cpu.instruction.bmi import BMI
from bitey.cpu.instruction.bne import BNE
from bitey.cpu.instruction.bpl import BPL
from bitey.cpu.instruction.brk import BRK
from bitey.cpu.instruction.bvc import BVC
from bitey.cpu.instruction.bvs import BVS
from bitey.cpu.instruction.clc import CLC
from bitey.cpu.instruction.cld import CLD
from bitey.cpu.instruction.cli import CLI
from bitey.cpu.instruction.clv import CLV
from bitey.cpu.instruction.cp import CMP
from bitey.cpu.instruction.cp import CPX
from bitey.cpu.instruction.cp import CPY
from bitey.cpu.instruction.dec import DEC
from bitey.cpu.instruction.dec import DEX
from bitey.cpu.instruction.dec import DEY
from bitey.cpu.instruction.eor import EOR
from bitey.cpu.instruction.inc import INC
from bitey.cpu.instruction.inc import INX
from bitey.cpu.instruction.inc import INY
from bitey.cpu.instruction.jmp import JMP
from bitey.cpu.instruction.jsr import JSR
from bitey.cpu.instruction.ld import LDA
from bitey.cpu.instruction.ld import LDX
from bitey.cpu.instruction.ld import LDY
from bitey.cpu.instruction.lsr import LSR
from bitey.cpu.instruction.nop import NOP
from bitey.cpu.instruction.ora import ORA
from bitey.cpu.instruction.pha import PHA
from bitey.cpu.instruction.php import PHP
from bitey.cpu.instruction.pla import PLA
from bitey.cpu.instruction.plp import PLP
from bitey.cpu.instruction.rol import ROL
from bitey.cpu.instruction.ror import ROR
from bitey.cpu.instruction.ror import RORNoCarryBug
from bitey.cpu.instruction.rti import RTI
from bitey.cpu.instruction.rts import RTS
from bitey.cpu.instruction.sbc import SBC, SBCCMOS, SBCNMOS
from bitey.cpu.instruction.sec import SEC
from bitey.cpu.instruction.sed import SED
from bitey.cpu.instruction.sei import SEI
from bitey.cpu.instruction.st import STA
from bitey.cpu.instruction.st import STX
from bitey.cpu.instruction.st import STY
from bitey.cpu.instruction.ta import TAX
from bitey.cpu.instruction.ta import TAY
from bitey.cpu.instruction.ta import TXA
from bitey.cpu.instruction.ta import TYA
from bitey.cpu.instruction.tsx import TSX
from bitey.cpu.instruction.txs import TXS


@dataclass
class InstructionFactory:
    instruction_map: ClassVar[dict[int, Instruction]] = {
        0: BRK,
        1: ORA,
        5: ORA,
        6: ASL,
        8: PHP,
        9: ORA,
        10: ASL,
        13: ORA,
        14: ASL,
        16: BPL,
        17: ORA,
        21: ORA,
        22: ASL,
        24: CLC,
        25: ORA,
        29: ORA,
        30: ASL,
        32: JSR,
        33: AND,
        36: BIT,
        37: AND,
        38: ROL,
        40: PLP,
        41: AND,
        42: ROL,
        44: BIT,
        45: AND,
        46: ROL,
        48: BMI,
        49: AND,
        53: AND,
        54: ROL,
        56: SEC,
        57: AND,
        61: AND,
        62: ROL,
        64: RTI,
        65: EOR,
        69: EOR,
        70: LSR,
        72: PHA,
        73: EOR,
        74: LSR,
        76: JMP,
        77: EOR,
        78: LSR,
        80: BVC,
        81: EOR,
        85: EOR,
        86: LSR,
        88: CLI,
        89: EOR,
        93: EOR,
        94: LSR,
        96: RTS,
        97: ADC,
        101: ADC,
        102: ROR,
        104: PLA,
        105: ADC,
        106: ROR,
        108: JMP,
        109: ADC,
        110: ROR,
        112: BVS,
        113: ADC,
        117: ADC,
        118: ROR,
        120: SEI,
        121: ADC,
        125: ADC,
        126: ROR,
        129: STA,
        132: STY,
        133: STA,
        134: STX,
        136: DEY,
        138: TXA,
        140: STY,
        141: STA,
        142: STX,
        144: BCC,
        145: STA,
        148: STY,
        149: STA,
        150: STX,
        152: TYA,
        153: STA,
        154: TXS,
        157: STA,
        160: LDY,
        161: LDA,
        162: LDX,
        164: LDY,
        165: LDA,
        166: LDX,
        168: TAY,
        169: LDA,
        170: TAX,
        172: LDY,
        173: LDA,
        174: LDX,
        176: BCS,
        177: LDA,
        180: LDY,
        181: LDA,
        182: LDX,
        184: CLV,
        185: LDA,
        186: TSX,
        188: LDY,
        189: LDA,
        190: LDX,
        192: CPY,
        193: CMP,
        196: CPY,
        197: CMP,
        198: DEC,
        200: INY,
        201: CMP,
        202: DEX,
        204: CPY,
        205: CMP,
        206: DEC,
        208: BNE,
        209: CMP,
        213: CMP,
        214: DEC,
        216: CLD,
        217: CMP,
        221: CMP,
        222: DEC,
        224: CPX,
        225: SBC,
        228: CPX,
        229: SBC,
        230: INC,
        232: INX,
        233: SBC,
        234: NOP,
        236: CPX,
        237: SBC,
        238: INC,
        240: BEQ,
        241: SBC,
        245: SBC,
        246: INC,
        248: SED,
        249: SBC,
        253: SBC,
        254: INC,
    }

    def __post_init__(self):
        "Initialize the InstructionFactory"
        self.logger = logging.getLogger(
            "bitey.cpu.instruction.instruction_factory.InstructionFactory"
        )

    def build(name, opcode, description, options={}):
        """
        Build an Instruction instance
        This builds an instruction from an instruction name, opcode and description.
        The opcode is an Opcode class.
        """
        try:
            inst = InstructionFactory.get_instruction_from_opcode(opcode)(
                name, opcode, description, options
            )
            return inst
        except UnimplementedInstruction:
            # Use the base class for the instruction
            # self.logger.debug("UnimplementedInstruction, building Instruction instance")
            return Instruction(name, opcode, description, options)

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
    instruction_map: ClassVar[dict[int, (InstructionClass, Instruction)]] = {
        0: BRK,
        1: ORA,
        5: ORA,
        6: ASL,
        8: PHP,
        9: ORA,
        10: ASL,
        13: ORA,
        14: ASL,
        16: BPL,
        17: ORA,
        21: ORA,
        22: ASL,
        24: CLC,
        25: ORA,
        29: ORA,
        30: ASL,
        32: JSR,
        33: AND,
        36: BIT,
        37: AND,
        38: ROL,
        40: PLP,
        41: AND,
        42: ROL,
        44: BIT,
        45: AND,
        46: ROL,
        48: BMI,
        49: AND,
        53: AND,
        54: ROL,
        56: SEC,
        57: AND,
        61: AND,
        62: ROL,
        64: RTI,
        65: EOR,
        69: EOR,
        70: LSR,
        72: PHA,
        73: EOR,
        74: LSR,
        76: JMP,
        77: EOR,
        78: LSR,
        80: BVC,
        81: EOR,
        85: EOR,
        86: LSR,
        88: CLI,
        89: EOR,
        93: EOR,
        94: LSR,
        96: RTS,
        97: ADC,
        101: ADC,
        102: ROR,
        104: PLA,
        105: ADC,
        106: ROR,
        108: JMP,
        109: ADC,
        110: ROR,
        112: BVS,
        113: ADC,
        117: ADC,
        118: ROR,
        120: SEI,
        121: ADC,
        125: ADC,
        126: ROR,
        129: STA,
        132: STY,
        133: STA,
        134: STX,
        136: DEY,
        138: TXA,
        140: STY,
        141: STA,
        142: STX,
        144: BCC,
        145: STA,
        148: STY,
        149: STA,
        150: STX,
        152: TYA,
        153: STA,
        154: TXS,
        157: STA,
        160: LDY,
        161: LDA,
        162: LDX,
        164: LDY,
        165: LDA,
        166: LDX,
        168: TAY,
        169: LDA,
        170: TAX,
        172: LDY,
        173: LDA,
        174: LDX,
        176: BCS,
        177: LDA,
        180: LDY,
        181: LDA,
        182: LDX,
        184: CLV,
        185: LDA,
        186: TSX,
        188: LDY,
        189: LDA,
        190: LDX,
        192: CPY,
        193: CMP,
        196: CPY,
        197: CMP,
        198: DEC,
        200: INY,
        201: CMP,
        202: DEX,
        204: CPY,
        205: CMP,
        206: DEC,
        208: BNE,
        209: CMP,
        213: CMP,
        214: DEC,
        216: CLD,
        217: CMP,
        221: CMP,
        222: DEC,
        224: CPX,
        225: SBC,
        228: CPX,
        229: SBC,
        230: INC,
        232: INX,
        233: SBC,
        234: NOP,
        236: CPX,
        237: SBC,
        238: INC,
        240: BEQ,
        241: SBC,
        245: SBC,
        246: INC,
        248: SED,
        249: SBC,
        253: SBC,
        254: INC,
    }
    # A custom instruction class map to hold buggy or quirky instructions
    instruction_map_options: ClassVar[
        dict[str, dict[int, (InstructionClass, Instruction)]]
    ] = {
        "no_carry_bug": {
            102: RORNoCarryBug,
            106: RORNoCarryBug,
            110: RORNoCarryBug,
            126: RORNoCarryBug,
        },
        "large_lower_nibble_behavior_1": {
            97: ADCNMOS,
            101: ADCNMOS,
            105: ADCNMOS,
            109: ADCNMOS,
            113: ADCNMOS,
            117: ADCNMOS,
            121: ADCNMOS,
            125: ADCNMOS,
            225: SBCNMOS,
            229: SBCNMOS,
            233: SBCNMOS,
            237: SBCNMOS,
            241: SBCNMOS,
            245: SBCNMOS,
            249: SBCNMOS,
            253: SBCNMOS,
        },
        "large_lower_nibble_behavior_2": {
            97: ADCCMOS,
            101: ADCCMOS,
            105: ADCCMOS,
            109: ADCCMOS,
            113: ADCCMOS,
            117: ADCCMOS,
            121: ADCCMOS,
            125: ADCCMOS,
            225: SBCCMOS,
            229: SBCCMOS,
            233: SBCCMOS,
            237: SBCCMOS,
            241: SBCCMOS,
            245: SBCCMOS,
            249: SBCCMOS,
            253: SBCCMOS,
        },
    }

    logger: ClassVar = logging.getLogger("bitey.cpu.instruction.instruction_factory")

    def __post_init__(self):
        "Initialize the InstructionFactory"
        self.logger = logging.getLogger(
            "bitey.cpu.instruction.instruction_factory.InstructionFactory"
        )

    def build(name, opcodes, description, options={}):
        """
        Build an Instruction instance
        This builds an instruction from an instruction name,
        list of opcodes and description.
        TODO: Refactor this
        """
        # TODO: Refactor this
        if len(opcodes.opcodes) > 0:
            opcode = opcodes.opcodes[0].opcode
            if options is not None:
                for key in options.keys():
                    if key in InstructionClassFactory.instruction_map_options:
                        custom_instruction_classes = (
                            InstructionClassFactory.instruction_map_options[key]
                        )
                        try:
                            if opcode in custom_instruction_classes:
                                instruction_class = custom_instruction_classes[opcode]
                                logger = logging.getLogger(
                                    "bitey.cpu.instruction.instruction_factory.InstructionFactory"
                                )
                                logger.debug(
                                    "Creating instruction for opcode: {}".format(opcode)
                                )
                                inst = instruction_class(
                                    name, opcodes, description, options
                                )
                                return InstructionClass(
                                    name, inst, opcodes, description, options
                                )
                            else:
                                raise UnimplementedInstruction
                        except UnimplementedInstruction:
                            return InstructionClass(
                                name, inst, opcodes, description, options
                            )
            try:
                instruction_class = (
                    InstructionClassFactory.get_instruction_class_from_opcode(opcode)
                )
                inst = instruction_class(name, opcodes, description, options)
                # TODO: There could be a separate InstructionClass for each
                # instruction variant, so they're built once and execution doesn't slow down
                return InstructionClass(name, inst, opcodes, description, options)
            except UnimplementedInstruction:
                # Use the base class for the instruction
                return InstructionClass(name, None, opcodes, description, options)
        else:
            return None

    def get_instruction_class_from_opcode(opcode):
        "Given an opcode string, return the instruction class"
        if opcode in InstructionClassFactory.instruction_map:
            inst = InstructionClassFactory.instruction_map[opcode]
            return inst
        else:
            raise UnimplementedInstruction
