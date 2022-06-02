from dataclasses import dataclass
from bitey.cpu.instruction.instruction import Instruction, IncompleteInstruction
from bitey.cpu.arch import EightBitArch


@dataclass
class SBCNMOS(Instruction):
    """
    SBC: Subtract Memory from Accumulator with Borrow

    This instruction subtracts the value of memory and carry from the
    accumulator.

    The carry flag acts as an inverted borrow, it is cleared after a
    subtraction if there is a borrow.  It is set if there is no
    borrow.  On a new subtraction operation, it should normally be set
    before calling SBC.

    There are differences between the CMOS and NMOS implementations.
    Wikipedia describes differences in the N, V and Z flags, but
    several emulators return different accumulator results depending
    on the chipset.

    These differences occur when invalid decimal values are passed to
    the SBC instruction.  Since it's unclear what the correct behavior
    should be, neither generation is necessarily buggy.

    The NMOS chipset occurs in more early 8-bit machines, so the
    default behavior is NMOS.

    Several sources were helpful in figuring out the 6502 SBC and
    decimal mode algorithms.

    The Western Design Center Programming the 65816 manual goes into a
    good description on why the carry flag is inverted (page 130).  It
    also explains what the overflow and carry flags represent for
    signed and unsigned arithmetic (page 135).

    The SBC calculations are based on ones in the Apple2Emu, AppleWin,
    Atari800 and VICE sources.  The Apple2Emu has clean, commented
    source for the SBC instruction.  Thanks below are from the
    AppleWin sources:

    "Thanks to Scott Hemphill for the verified CMOS ADC and SBC
    algorithm! You rock.

    "And thanks to the VICE team for the NMOS ADC and SBC algorithms
    as well as the algorithms for those illops which involve ADC or
    SBC. You rock too."

    """

    def instruction_execute(self, cpu, memory, value, address):
        """
        SBC: Subtract Memory from Accumulator with Borrow

        This instruction subtracts the value of memory and carry from the
        accumulator.
        """
        if cpu.flags["D"].status is False:
            # Normal binary addition
            if value is not None:
                self.value = value
                self.carry_value = 0 if cpu.flags["C"].status else 1
                self.accumulator_value = cpu.registers["A"].get()
                # One's complement for following two's complement subtraction
                # self.complemented_value = 0xFF - self.value

                # # Two's complement value
                # self.twos_complement = self.complemented_value + self.carry_value

                # # Subtraction using addition and two's complement representation
                # self.result = self.accumulator_value + self.twos_complement

                self.result = self.accumulator_value - self.value - self.carry_value

                self.binary_result = self.result

                cpu.registers["A"].set(self.result & 0xFF)

                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction
        else:
            # Decimal mode addition
            # TODO: Simplify
            if value is not None:
                self.value = value
                self.carry_value = 0 if cpu.flags["C"].status else 1
                self.accumulator_value = cpu.registers["A"].get()
                self.result = self.accumulator_value - self.value - self.carry_value

                self.binary_result = self.result

                # The carry and overflow bits are set based on the full subtraction
                self.full_result = (
                    self.accumulator_value
                    + ((0xFF - self.value) & 0xFF)
                    + self.carry_value
                )

                # Subtract the nibbles one at a time
                # First subtract the low nibbles
                self.result = (
                    EightBitArch.low_nibble(self.accumulator_value)
                    - EightBitArch.low_nibble(self.value)
                    - self.carry_value
                )

                if (self.result & 0x10) != 0:
                    self.result = ((self.result - 0x06) & 0x0F) - 0x10
                self.result += (self.accumulator_value & 0xF0) - (self.value & 0xF0)

                if self.result & 0x100:
                    self.result -= 0x60

                cpu.registers["A"].set(self.result & 0xFF)

                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction

    def set_flags(self, flags, registers):  # noqa: C901
        if flags["D"].status is False:
            # binary mode subtraction
            if self.result is not None:
                # Set the carry flag
                if self.result < 0x00:
                    flags["C"].clear()
                else:
                    flags["C"].set()

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

                # Can be calculated from accumulator and memory, forms a
                # "triangular" distribution, e.g. with CLC set
                # 1 0xFE, 1 0x00, 2 0x01, 2 0xFD, ... 127 0x80
                # 1 0xFE, 1 0x00, 2 0x01, 2 0xFD, ... 127 0x80
                # To find number available, something like: 0x80 - abs(0x80 - NUM)
                # Then the numbers from 0x7F (or 0x80) down to 0x7F minus the number available
                # verify something like this, add tests around carry and edge cases
                # 0x00 endpoint is 0x80, 0xFE endpoint is 0x7F,
                # simple addition or "shift" should fix it
                # if abs(0x80 - self.value) < (0x80 - abs(0x80 - self.accumulator_value))
                #
                # Another way of calculating this is with bit seven in the
                # accumulator, memory and binary result.
                # fmt: off
                if (
                        (((self.accumulator_value & 0x80) == 0x80)
                         and ((self.value & 0x80) != 0x80)
                         and ((self.binary_result & 0x80) != 0x80))
                        or
                        (((self.accumulator_value & 0x80) != 0x80)
                         and ((self.value & 0x80) == 0x80)
                         and ((self.binary_result & 0x80) == 0x80))
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
                # fmt: on
        else:
            # decimal mode subtraction flags
            # The behavior of the V flag is "undocumented", but the behavior here
            # should follow the behavior of NMOS 6502 chips
            # The values below follows the values in the
            # transistor-level simulation found in visual6502.org
            # thse flags (C, Z, V, N) follow the same rules as for binary mode
            # It uses the binary addition result in calculating them too
            # "Verified" with the visual6502.org simulator
            #
            # Also documented in https://http://www.6502.org/tutorials/decimal_mode.html
            #
            # Although this document has an error:
            # the V flag is clear when the result is in the range -128
            # to 127 inclusive and set when the result is outside that
            # range.
            if self.result is not None:
                # Set the carry flag
                if self.binary_result < 0x00:
                    flags["C"].clear()
                else:
                    flags["C"].set()

                # Set the zero flag if the accumlator is zero
                if self.binary_result == 0x00:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()

                # Set the negative flag
                if (self.binary_result & 0x80) != 0:
                    flags["N"].set()
                else:
                    flags["N"].clear()

                # Can be calculated from accumulator and memory, forms a
                # "triangular" distribution , e.g. with CLC set
                # 1 0xFE, 1 0x00, 2 0x01, 2 0xFD, ... 127 0x80
                # To find number available, something like: 0x80 - abs(0x80 - NUM)
                # Then the numbers from 0x7F (or 0x80) down to 0x7F minus the number available
                # verify something like this, add tests around carry and edge cases
                # 0x00 endpoint is 0x80, 0xFE endpoint is 0x7F,
                # simple addition or "shift" should fix it
                # if abs(0x80 - self.value) < (0x80 - abs(0x80 - self.accumulator_value))
                #
                # Another way of calculating this is with bit seven in the
                # accumulator, memory and binary result.
                # fmt: off
                if (
                        (((self.accumulator_value & 0x80) == 0x80)
                         and ((self.value & 0x80) != 0x80)
                         and ((self.binary_result & 0x80) != 0x80))
                        or
                        (((self.accumulator_value & 0x80) != 0x80)
                         and ((self.value & 0x80) == 0x80)
                         and ((self.binary_result & 0x80) == 0x80))
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
                # fmt: on


@dataclass
class SBCCMOS(Instruction):
    """
    SBC: Subtract Memory from Accumulator with Borrow

    This instruction subtracts the value of memory and carry from the
    accumulator.

    The carry flag acts as an inverted borrow, it is cleared after a
    subtraction if there is a borrow.  It is set if there is no
    borrow.  On a new subtraction operation, it should normally be set
    before calling SBC.

    There are differences between the CMOS and NMOS implementations.
    Wikipedia describes differences in the N, V and Z flags, but
    several emulators return different accumulator results depending
    on the chipset.

    Several sources were helpful in figuring out the 6502 SBC and
    decimal mode algorithms.

    The Western Design Center Programming the 65816 manual goes into a
    good description on why the carry flag is inverted (page 130).  It
    also explains what the overflow and carry flags represent for
    signed and unsigned arithmetic (page 135).

    The SBC calculations are based on ones in the Apple2Emu, AppleWin,
    Atari800 and VICE sources.  The Apple2Emu has clean, commented
    source for the SBC instruction.  Thanks below are from the
    AppleWin sources:

    "Thanks to Scott Hemphill for the verified CMOS ADC and SBC
    algorithm! You rock.

    "And thanks to the VICE team for the NMOS ADC and SBC algorithms
    as well as the algorithms for those illops which involve ADC or
    SBC. You rock too."

    """

    def instruction_execute(self, cpu, memory, value, address):
        """
        SBC: Subtract Memory from Accumulator with Borrow

        This instruction subtracts the value of memory and carry from the
        accumulator.
        """
        if cpu.flags["D"].status is False:
            # Normal binary addition
            if value is not None:
                self.value = value
                self.carry_value = 1 if cpu.flags["C"].status else 0
                self.accumulator_value = cpu.registers["A"].get()
                # One's complement for following two's complement subtraction
                self.complemented_value = 0xFF - self.value
                self.twos_complement = self.complemented_value + self.carry_value

                self.result = self.accumulator_value + self.twos_complement

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

                # The carry and overflow bits are set based on the full subtraction
                self.full_result = (
                    self.accumulator_value
                    + ((0xFF - self.value) & 0xFF)
                    + self.carry_value
                )
                self.result = (
                    self.accumulator_value
                    + ((0xFF - self.value) & 0xFF)
                    + self.carry_value
                )

                # Subtract the nibbles one at a time
                # First subtract the low nibbles
                self.al = (
                    EightBitArch.low_nibble(self.accumulator_value)
                    - EightBitArch.low_nibble(self.value)
                    + self.carry_value
                    - 1
                )

                self.result = self.accumulator_value - self.value + self.carry_value - 1
                if self.result < 0:
                    self.result = self.result - 0x60

                if self.al < 0:
                    self.result = self.result - 0x06

                cpu.registers["A"].set(self.result & 0xFF)

                self.set_flags(cpu.flags, cpu.registers)
            else:
                self.value = None
                self.result = None
                raise IncompleteInstruction

    def set_flags(self, flags, registers):  # noqa: C901
        if flags["D"].status is False:
            # binary mode subtraction
            if self.result is not None:
                # Set the carry flag
                if self.result < 0x100:
                    flags["C"].clear()
                else:
                    flags["C"].set()

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

                # if (self.accumulator_value & 0x80) != (self.value & 0x80) and (
                #     self.accumulator_value & 0x80
                # ) != (registers["A"].get() & 0x80):
                if (
                    (self.accumulator_value ^ self.value)
                    & (self.accumulator_value ^ self.result)
                    & 0x80
                ):
                    flags["V"].set()
                else:
                    flags["V"].clear()
        else:
            # decimal mode subtraction
            # TODO: Verify C flag and others in emulator and manual
            # The C and V flags are based on the result of the "full" subtraction
            # This may not be the case for real hardware, but in some emulators such
            # such as apple2emu, this is the case.
            if self.full_result is not None:
                if (self.accumulator_value & 0x80) != (self.value & 0x80) and (
                    self.accumulator_value & 0x80
                ) != (self.full_result & 0x80):
                    flags["V"].set()
                else:
                    flags["V"].clear()

            if self.result is not None:
                # From the MCS6500 Family Programming Manual:
                # The carry flag is set if the result is greater than or equal to zero
                # Otherwise it is reset
                if self.result >= 0:
                    flags["C"].set()
                else:
                    flags["C"].clear()

                if registers["A"].get() & 0x80:
                    flags["N"].set()
                else:
                    flags["N"].clear()

                if registers["A"].get() == 0x00:
                    flags["Z"].set()
                else:
                    flags["Z"].clear()


class SBC(SBCNMOS):
    pass


class SBCLargeLowerNibbleBehavior(SBCNMOS):
    pass
