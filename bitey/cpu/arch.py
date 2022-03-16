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
