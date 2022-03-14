from bitey.cpu.flag.flag import Flag, Flags
from bitey.cpu.flag.flag_json_decoder import FlagsJSONDecoder
from bitey.cpu.flag.zero_flag import ZeroFlag
from bitey.cpu.register import Register


def test_cpu_flag_init():
    f = Flag("C", "Carry", 0, False)
    assert f.short_name == "C"
    assert f.name == "Carry"
    assert f.bit_field_pos == 0


def test_cpu_flags_init():
    f1 = Flag("C", "Carry", 0, False)
    f2 = Flag("Z", "Zero Result", 1, False)
    flags = Flags([f1, f2], 0)
    assert len(flags.flags) == 2
    assert type(flags.data) == int
    assert flags.data == 0
    assert flags["C"] == f1
    assert flags["Z"] == f2


def test_cpu_flags_post_init():
    f1 = Flag("C", "Carry", 0, False)
    f2 = Flag("Z", "Zero Result", 1, False)
    flags = Flags([f1, f2], 0)
    assert len(flags.flags) == 2
    assert type(flags.data) == int
    assert flags.data == 0
    assert flags["C"] == f1
    assert flags["Z"] == f2

    assert flags["C"].flags == flags
    assert flags["Z"].flags == flags


def test_cpu_flags_set():
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2

    flags.data = 0

    assert flags["C"].status is False

    # Try setting the C flag
    flags.set("C")

    assert flags.data == 1
    assert flags["C"].status is True

    assert flags.data == 1
    assert flags["Z"].status is False

    # Try setting the Z flag
    flags.set("Z")

    assert flags.data == 3
    assert flags["C"].status is True

    assert flags.data == 3
    assert flags["Z"].status is True

    # Try clearing the C flag
    flags.clear("C")

    assert flags.data == 2
    assert flags["C"].status is False

    assert flags.data == 2
    assert flags["Z"].status is True


def test_cpu_flags_flag_set():
    # Test setting and clearing flags via individual flag interface
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2

    flags.data = 0

    assert flags["C"].status is False

    # Try setting the C flag
    flags["C"].set()

    assert flags.data == 1
    assert flags["C"].status is True

    assert flags.data == 1
    assert flags["Z"].status is False

    # Try setting the Z flag
    flags["Z"].set()

    assert flags.data == 3
    assert flags["C"].status is True

    assert flags.data == 3
    assert flags["Z"].status is True

    # Try clearing the C flag
    flags["C"].clear()

    assert flags.data == 2
    assert flags["C"].status is False

    assert flags.data == 2
    assert flags["Z"].status is True


def test_cpu_flags_json_decoder():
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2


def test_cpu_flags_zero_flag():
    z = ZeroFlag("Z", "Zero Result", 1, 0)
    assert not z.status

    a_register = Register("A", "Accumulator", 8, 0)

    assert a_register.value == 0
    assert a_register == 0
    z.test_register_result(a_register)

    assert z.status

def test_cpu_flags_zero_flag_updates_flags():
    "Test that updating the zero flag updates the flags bit field"
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2

    zero_flag = flags["Z"]

    assert not zero_flag.status
    assert not (flags.data & 0b00000010) == 0b00000010

    a_register = Register("A", "Accumulator", 8, 0)

    assert a_register.value == 0
    assert a_register == 0
    zero_flag.test_register_result(a_register)

    assert zero_flag.status

    assert (flags.data & 0b00000010) == 0b00000010

def test_cpu_flags_negative_flag_updates_flags():
    "Test that updating the negative flag updates the flags bit field"
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    },
    {
        "short_name": "N",
        "name": "Negative Result",
        "bit_field_pos": 7,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 3

    negative_flag = flags["N"]

    assert not negative_flag.status
    assert not (flags.data & 0b10000000) == 0b10000000

    a_register = Register("A", "Accumulator", 8, 0x83)

    assert a_register.value == 0x83
    assert a_register == 0x83
    negative_flag.test_register_result(a_register)

    assert negative_flag.status

    assert (flags.data & 0b10000000) == 0b10000000


def test_cpu_flags_flags_set_updates_zero_flag():
    "Test that updating the zero flag updates the flags bit field"
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2

    zero_flag = flags["Z"]

    assert not zero_flag.status
    assert not (flags.data & 0b00000010) == 0b00000010

    flags.set("Z")

    assert zero_flag.status

    assert (flags.data & 0b00000010) == 0b00000010

def test_cpu_flags_flags_set_updates_negative_flag():
    "Test that updating the negative flag updates the flags bit field"
    s = """
    [
    {
        "short_name": "C",
        "name": "Carry",
        "bit_field_pos": 0,
        "status": 0
    },
    {
        "short_name": "Z",
        "name": "Zero Result",
        "bit_field_pos": 1,
        "status": 0
    },
    {
        "short_name": "N",
        "name": "Negative Result",
        "bit_field_pos": 7,
        "status": 0
    }
    ]
    """
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 3

    negative_flag = flags["N"]

    assert not negative_flag.status
    assert not (flags.data & 0b10000000) == 0b10000000

    flags.set("N")

    assert negative_flag.status == True

    assert (flags.data & 0b10000000) == 0b10000000
