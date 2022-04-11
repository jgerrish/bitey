from dataclasses import dataclass
from bitey.cpu.instruction.instruction import (
    Instruction,
    IncompleteInstruction,
)
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
        """
        if (
            options is not None
            and ("page_boundary_bug" in options)
            and (options["page_boundary_bug"] is True)
        ):
            # Replace the addressing mode if this is an old JMP
            # TODO: Still need to fix this pattern, the environment isn't good
            for opc in opcode:
                if type(opc.addressing_mode) == AbsoluteIndirectAddressingMode:
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
