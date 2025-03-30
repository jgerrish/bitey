from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction
from bitey.cpu.instruction.incomplete_instruction import IncompleteInstruction
from bitey.cpu.arch import EightBitArch


@dataclass
class ADCNMOS(Instruction):
    """
    ADC: Add Memory to Accumulator with Carry

    This instruction adds the value of memory and carry to the value
    of the accumulator.

    There are differences between the CMOS and NMOS implementations.
    Wikipedia describes differences in the N, V and Z flags, but
    several emulators return different accumulator results depending
    on the chipset.

    Several sources were helpful in figuring out the 6502 SBC and
    decimal mode algorithms.

    In addition to the official MCS6500 Family Programming Manual,
    there are several books and articles that were useful.

    Apple Machine Language by Don Inman and Kurt Inman has several
    examples of decimal mode arithmetic.

    John West and Marko MŠkelŠ have a document describing Decimal mode
    in NMOS 6500 series in depth and other processor features.  It
    includes more heavily commented versions of the code below.  The
    name of the document is "Documentation for the NMOS 65xx/85xx
    Instruction Set."

    The ADC and SBC calculations are based on ones in the Apple2Emu,
    AppleWin, Atari800 and VICE sources.  The Apple2Emu has clean,
    commented source for the SBC instruction.  Thanks below are from
    the AppleWin sources:

    "Thanks to Scott Hemphill for the verified CMOS ADC and SBC
    algorithm! You rock.

    "And thanks to the VICE team for the NMOS ADC and SBC algorithms
    as well as the algorithms for those illops which involve ADC or
    SBC. You rock too."

    """

    def instruction_execute(self, cpu, memory, value, address):
        """
        ADC: Add Memory to Accumulator with Carry

        This instruction adds the value of memory and carry to the value
        of the accumulator.
        """
        if cpu.flags["D"].status is False:
            # Normal binary addition
            if value is not None:
                self.value = value
                self.carry_value = 1 if cpu.flags["C"].status else 0
                self.accumulator_value = cpu.registers["A"].get()
                self.result = self.accumulator_value + self.value + self.carry_value
                cpu.registers["A"].set(self.result & 0xFF)
                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction
        else:
            # Decimal mode addition
            if value is not None:
                self.value = value
                self.carry_value = 1 if cpu.flags["C"].status else 0
                self.accumulator_value = cpu.registers["A"].get()
                self.binary_addition_result = (
                    self.accumulator_value + self.value + self.carry_value
                )

                # Add the nibbles one at a time
                # First add the low nibbles
                self.result = (
                    EightBitArch.low_nibble(self.accumulator_value)
                    + EightBitArch.low_nibble(self.value)
                    + self.carry_value
                )

                # Decimal addition doesn't allow values greater than 9 in either nibble
                if self.result >= 10:
                    # "Bump" the extra result over to the next nibble
                    # ((self.result + 0x06) & 0x0F) masks out the tens
                    # ((self.result + 0x06) & 0x0F) + 0x10 masks out the tens and adds
                    # the decimal carry from the low nibble
                    self.result = ((self.result + 0x06) & 0x0F) + 0x10

                # Add the high nibbles
                self.result += (self.accumulator_value & 0xF0) + (self.value & 0xF0)

                # The chips set the sign bit based on the result up to here
                self.sign_bit_result = self.result

                # If the value in the high nibble is greater than 9, bump the result
                # 0xA0 -> 0b1010 0000, 0b1010 is 10
                if self.result >= 0xA0:
                    self.result += 0x60

                cpu.registers["A"].set(self.result & 0xFF)

                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction

    def set_flags(self, flags, registers):  # noqa: C901
        if flags["D"].status is False:
            # binary mode addition
            if self.result is not None:
                # Set the carry flag
                if self.result > 0xFF:
                    flags["C"].set()
                else:
                    flags["C"].clear()

                # Set the zero flag if the accumlator is zero
                if registers["A"].get() == 0x00:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()

                # Set the sign flag
                if (self.result & 0x80) != 0:
                    flags["N"].set()
                else:
                    flags["N"].clear()

                # Set the overflow flag if bit seven changed
                # The rule is, set the overflow if:
                # Both the operands are < 0x80 and the result is > 0x80, or
                # Both the operands are > 0x80 and the result is < 0x80
                # Inefficient, could be optimized
                # fmt: off
                if (
                        (((self.accumulator_value >= 0x80)
                          and (self.value >= 0x80))
                         and (registers["A"].get() < 0x80))
                        or
                        (((self.accumulator_value < 0x80)
                          and (self.value < 0x80))
                         and (registers["A"].get() >= 0x80))
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
                # fmt: on
        else:
            # decimal mode addition
            if self.result is not None:
                # Set the carry flag
                if self.result > 0x99:
                    flags["C"].set()
                else:
                    flags["C"].clear()

                # Set the sign flag
                # For NMOS chips, this is based on the binary addition result
                if (self.sign_bit_result & 0x80) != 0:
                    flags["N"].set()
                else:
                    flags["N"].clear()

                # Set the zero flag
                # For NMOS chips, this is based on the binary addition result
                if (self.binary_addition_result & 0xFF) == 0:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()

                # Set the overflow flag if bit seven changed
                # For NMOS chips, this is based on the binary addition result
                # fmt: off
                if (
                        ((self.accumulator_value ^ self.sign_bit_result) & 0x80)
                        and (not ((self.accumulator_value ^ self.value) & 0x80))
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
                # fmt: on


@dataclass
class ADCCMOS(Instruction):
    """
    ADC: Add Memory to Accumulator with Carry

    This instruction adds the value of memory and carry to the value
    of the accumulator.

    There are differences between the CMOS and NMOS implementations.
    Wikipedia describes differences in the N, V and Z flags, but
    several emulators return different accumulator results depending
    on the chipset.

    Several sources were helpful in figuring out the 6502 SBC and
    decimal mode algorithms.

    In addition to the official MCS6500 Family Programming Manual,
    there are several books and articles that were useful.

    Apple Machine Language by Don Inman and Kurt Inman has several
    examples of decimal mode arithmetic.

    John West and Marko MŠkelŠ have a document describing Decimal mode
    in NMOS 6500 series in depth and other processor features.  It
    includes more heavily commented versions of the code below.  The
    name of the document is "Documentation for the NMOS 65xx/85xx
    Instruction Set."

    The ADC and SBC calculations are based on ones in the Apple2Emu,
    AppleWin, Atari800 and VICE sources.  The Apple2Emu has clean,
    commented source for the SBC instruction.  Thanks below are from
    the AppleWin sources:

    "Thanks to Scott Hemphill for the verified CMOS ADC and SBC
    algorithm! You rock.

    "And thanks to the VICE team for the NMOS ADC and SBC algorithms
    as well as the algorithms for those illops which involve ADC or
    SBC. You rock too."

    """

    def instruction_execute(self, cpu, memory, value, address):
        """
        ADC: Add Memory to Accumulator with Carry

        This instruction adds the value of memory and carry to the value
        of the accumulator.
        """
        if cpu.flags["D"].status is False:
            # Normal binary addition
            if value is not None:
                self.value = value
                self.carry_value = 1 if cpu.flags["C"].status else 0
                self.accumulator_value = cpu.registers["A"].get()
                self.result = self.accumulator_value + self.value + self.carry_value
                cpu.registers["A"].set(self.result & 0xFF)
                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction
        else:
            # Decimal mode addition
            if value is not None:
                self.value = value
                self.carry_value = 1 if cpu.flags["C"].status else 0
                self.accumulator_value = cpu.registers["A"].get()

                # Add the nibbles one at a time
                # First add the low nibbles
                self.result = (
                    EightBitArch.low_nibble(self.accumulator_value)
                    + EightBitArch.low_nibble(self.value)
                    + self.carry_value
                )

                # Decimal addition doesn't allow values greater than 9 in either nibble
                if self.result >= 10:
                    # "Bump" the extra result over to the next nibble
                    # ((self.result + 0x06) & 0x0F) masks out the tens
                    # ((self.result + 0x06) & 0x0F) + 0x10 masks out the tens and adds
                    # the decimal carry from the low nibble
                    self.result = ((self.result + 0x06) & 0x0F) + 0x10

                # Add the high nibbles
                self.result += (self.accumulator_value & 0xF0) + (self.value & 0xF0)

                # The chips set the sign bit based on the result up to here
                self.sign_bit_result = self.result

                # If the value in the high nibble is greater than 9, bump the result
                # 0xA0 -> 0b1010 0000, 0b1010 is 10
                if self.result >= 0xA0:
                    self.result += 0x60

                cpu.registers["A"].set(self.result & 0xFF)

                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction

    def set_flags(self, flags, registers):  # noqa: C901
        if flags["D"].status is False:
            # binary mode addition
            if self.result is not None:
                # Set the carry flag
                if self.result > 0xFF:
                    flags["C"].set()
                else:
                    flags["C"].clear()

                # Set the zero flag if the accumlator is zero
                if registers["A"].get() == 0x00:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()

                # Set the negative flag
                if (registers["A"].get() & 0x80) != 0:
                    flags["N"].set()
                else:
                    flags["N"].clear()
                # Set the overflow flag

                # This behavior was modified several times
                # The current behavior is described right above the conditional
                # It's based on simulations with the visual6502.org
                # transistor-level simulator

                # The previous, possibly incorrect behavior is described below

                # This interpretation of the V flag should be compared against
                # actual hardware
                # This comparison is made in the SBC instruction too
                # This is based on logic from apple2emu and AppleWin
                # The last 0x80 mask indicates we're only indicated in bit seven
                # Here's a simple addition table of several two two-bit signed numbers
                # to show how this comparison works, using 0x02 (0b10) as the mask:
                # A:    00    01    00    10    11    01
                # M:  + 00  + 00  + 01  + 00  + 01  + 11
                #       --    --    --    --    --    --
                #       00    01    01    10   100   100
                #
                # V:     0     0     0     0     1     0
                # In particular, note it's not symmetric,
                # the accumlator bit change is what is checked.
                # If the accumulator is 0b01 and the memory is 0b11,
                # V is 0, but if the accumulator is 0b11 and the memory is 0b01,
                # V is 1

                # The current behavior uses transistor-level models from
                # visual6502.org
                # These simulations may be inaccurate or have bugs, they haven't
                # been verified against hardware runs.
                #
                # An assembly language program to run all possible combinations of
                # adds is included in the examples directory
                # Simply change CLD, SEC and ADC to try other combinations
                #
                # The behavior of the V flag in ADC decimal mode isn't a simple
                # "triangular" reflection, but a triangular reflection with a
                # series of spikes or "plates" on one edge and a series of
                # indentations on the other edge.

                # The rule is, set the overflow if:
                # Both the operands are < 0x80 and the result is > 0x80, or
                # Both the operands are > 0x80 and the result is < 0x80
                # Inefficient, could be optimized

                # This uses the following rule:
                # The rule is, set the overflow if:
                # Both the operands are < 0x80 and the result is > 0x80, or
                # Both the operands are > 0x80 and the result is < 0x80
                # fmt: off
                if (
                        (((self.accumulator_value >= 0x80)
                          and (self.value >= 0x80))
                         and (registers["A"].get() < 0x80))
                        or
                        (((self.accumulator_value < 0x80)
                          and (self.value < 0x80))
                         and (registers["A"].get() >= 0x80))
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
                # fmt: on
        else:
            # decimal mode addition
            if self.result is not None:
                # Set the carry flag
                if self.result > 0x99:
                    flags["C"].set()
                else:
                    flags["C"].clear()

                # Set the sign flag
                if (self.result & 0x80) != 0:
                    flags["N"].set()
                else:
                    flags["N"].clear()

                # These flags are set differently on CMOS
                # Set the zero flag
                # For CMOS chips, this is based on the final addition result
                if (self.result & 0xFF) == 0:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()

                # Overflow flag is set if result is greater than what a signed
                # representation can hold
                if self.result >= 0x80:
                    flags["V"].set()
                else:
                    flags["V"].clear()


class ADC(ADCNMOS):
    pass
