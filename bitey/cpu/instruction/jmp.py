from dataclasses import dataclass
import logging


from bitey.cpu.instruction.instruction import Instruction
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.addressing_mode import (
    AbsoluteIndirectAddressingMode,
    AbsoluteIndirectPageBoundaryBugAddressingMode,
)


@dataclass
class JMP(Instruction):
    """
    JMP: Jump to New Location

    Some versions of the NMOS 6502 chip had buggy absolute indirect addressing
    JMP instructions.  If the base address was on a page boundary
    (xyFF for the ADL) it would get the next address from the beginning of that page
    instead of the beginning of the next page.  It would use xy00 instead of xz00.
    """

    def __init__(self, name, opcode, description, options={}):
        """
        Override addressing mode if this instruction is from an older 6502

        We've refactored the options JSON dictionary / hash to have a
        "bugs" key.  This new config data structure can be used to
        pragmatically patch bugs in different areas of the emulator.

        For example, if the options key exists in an instruction like
        JMP, and there are bugs and the patch key is true, we will call a patch_bug()
        method on the JMP Instruction subclass.

        It will no longer need to be part of __init__
        """
        if (
            options is not None
            and ("bugs" in options)
            and ("page_boundary_bug" in options["bugs"])
            and ("exists" in options["bugs"]["page_boundary_bug"])
            and (options["bugs"]["page_boundary_bug"]["exists"] is True)
            and ("patch" in options["bugs"]["page_boundary_bug"])
        ):
            # Replace the addressing mode if this is an old JMP
            # TODO: Still need to fix this pattern
            #
            # TODO: Fix opcode variable name
            # I think the "opcode" variable is named wrong
            # If we're iterating through opcode, it's probably an Opcode class and the variable
            # should be named opcodes
            #
            #
            # Ok, there are a bunch of issues with this code.
            #
            # First, we're using isinstance when we should be using a
            # subclassed method.
            self.logger = logging.getLogger("bitey.cpu.instruction.jmp")
            for opc in opcode:
                if isinstance(opc.addressing_mode, AbsoluteIndirectAddressingMode):
                    self.logger.debug(
                        "Setting addressing mode to AbsoluteIndirectPageBoundaryBugAddressingMode"
                    )

                    opc.addressing_mode = AbsoluteIndirectPageBoundaryBugAddressingMode(
                        3
                    )
        super().__init__(name, opcode, description, options)

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, jumping to the new location
        """
        if address is not None:
            cpu.registers["PC"].set(address)
        else:
            raise IncompleteInstruction


class JMPPageBoundaryBug(Instruction):
    """
    JMP: Jump to New Location

    Some versions of the NMOS 6502 chip had buggy absolute indirect addressing
    JMP instructions.  If the base address was on a page boundary
    (xyFF for the ADL) it would get the next address from the beginning of that page
    instead of the beginning of the next page.  It would use xy00 instead of xz00.

    This version of the instruction exhibits that behavior.
    """

    def instruction_execute(self, cpu, memory, value, address=None):
        """
        Execute the instruction, jumping to the new location
        """
        if address is not None:
            cpu.registers["PC"].set(address)
        else:
            raise IncompleteInstruction
