from bitey.cpu.arch import EightBitArch, IntegerValueError


def test_cpu_cpu_signed_int_to_twos_complement():
    "Test conversion from signed int to single-byte twos complement works"
    assert EightBitArch.signed_int_to_twos_complement(0) == 0x00
    assert EightBitArch.signed_int_to_twos_complement(1) == 0x01
    assert EightBitArch.signed_int_to_twos_complement(2) == 0x02
    assert EightBitArch.signed_int_to_twos_complement(127) == 0x7F
    try:
        EightBitArch.signed_int_to_twos_complement(128)
        assert False
    except IntegerValueError:
        assert True

    assert EightBitArch.signed_int_to_twos_complement(-1) == 0xFF
    assert EightBitArch.signed_int_to_twos_complement(-2) == 0xFE
    assert EightBitArch.signed_int_to_twos_complement(-128) == 0x80
    try:
        EightBitArch.signed_int_to_twos_complement(-129)
        assert False
    except IntegerValueError:
        assert True


def test_cpu_cpu_twos_complement_to_signed_int():
    "Test conversion from single-byte twos complmented to signed int works"
    assert EightBitArch.twos_complement_to_signed_int(0x00) == 0
    assert EightBitArch.twos_complement_to_signed_int(0x01) == 1
    assert EightBitArch.twos_complement_to_signed_int(0x02) == 2
    assert EightBitArch.twos_complement_to_signed_int(0x7F) == 127
    try:
        EightBitArch.twos_complement_to_signed_int(-1)
    except IntegerValueError:
        assert True

    assert EightBitArch.twos_complement_to_signed_int(0xFF) == -1
    assert EightBitArch.twos_complement_to_signed_int(0xFE) == -2
    assert EightBitArch.twos_complement_to_signed_int(0x80) == -128
    try:
        EightBitArch.twos_complement_to_signed_int(0x100)
    except IntegerValueError:
        assert True
