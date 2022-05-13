"""
Architecture-level classes and functions
These can be shared between chips
"""


class IntegerValueError(Exception):
    """
    Represents an exception when the argument to a function is an invalid value.
    For example, it may be too small or too large.
    """


class EightBitArch:
    def high_nibble(byte):
        """
        Get the high nibble of a byte
        """
        return (byte >> 4) & 0x0F

    def low_nibble(byte):
        """
        Get the low nibble of a byte
        """
        return byte & 0x0F

    def decimal_value(byte):
        """
        Get the 4-bit Binary Coded Decimal (BCD) value of a byte
        The decimal value of a byte is found by "concatenating" the
        high nibble and low nibble, or adding them after multiplying
        the high nibble by ten.
        """
        return (EightBitArch.high_nibble(byte) * 10) + EightBitArch.low_nibble(byte)

    def signed_int_to_twos_complement(signed_int_value):
        """
        Convert a signed integer to a single-byte two's-complement value
        """
        # The range of negative values represented in two's complement stored
        # in a single byte is -128 to 127 inclusive
        if (signed_int_value < -128) or (signed_int_value > 127):
            raise IntegerValueError

        if signed_int_value < 0:
            twos_complement_value = (0xFF - abs(signed_int_value)) + 1
        else:
            twos_complement_value = signed_int_value

        return twos_complement_value

    def twos_complement_to_signed_int(twos_complement_value):
        """
        Convert a single-byte negative value represented as
        two's-complement to a signed integer value.
        """
        if (twos_complement_value < 0x00) or (twos_complement_value > 0xFF):
            raise IntegerValueError

        if twos_complement_value > 0x7F:
            # Calculate two's complement to get negative value
            signed_int_value = -((0xFF - twos_complement_value) + 1)
        else:
            signed_int_value = twos_complement_value

        return signed_int_value
