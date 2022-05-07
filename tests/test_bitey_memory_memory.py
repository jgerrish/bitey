from bitey.memory.memory import Memory, MemoryOutOfRange


def test_memory_init():
    memory = Memory()
    assert str(type(memory.memory)) == "<class 'bytearray'>"
    assert len(memory.memory) == 0

    memory = Memory(2 ** 16)
    assert len(memory.memory) == 65536


def test_memory_get_16bit_value():
    memory = Memory(2 ** 16)
    assert len(memory.memory) == 65536

    # Test zero case
    memory.write(0, 0)
    memory.write(1, 0)
    value = memory.get_16bit_value(0, 1)
    assert value == 0

    # Test zero adl
    memory.write(0, 0)
    memory.write(1, 3)
    value = memory.get_16bit_value(0, 1)
    assert value == 768

    # Test zero adh
    memory.write(0, 3)
    memory.write(1, 0)
    value = memory.get_16bit_value(0, 1)
    assert value == 3

    # Test other value
    memory.write(0, 10)
    memory.write(1, 3)

    value = memory.get_16bit_value(0, 1)
    assert value == 778


def test_memory_memory_out_of_range():
    memory = Memory(2 ** 16)
    assert len(memory.memory) == 65536

    # Try at beginning of memory
    try:
        memory.read(0)
        assert True
    except MemoryOutOfRange:
        assert False

    # Try before valid memory
    try:
        memory.read(-1)
        assert False
    except MemoryOutOfRange:
        assert True

    # Try at end of memory
    try:
        memory.read(65535)
        assert True
    except MemoryOutOfRange:
        assert False

    # Try after valid memory
    try:
        memory.read(65536)
        assert False
    except MemoryOutOfRange:
        assert True


def test_memory_memory_read_range():
    memory = Memory(2 ** 16)
    assert len(memory.memory) == 65536

    # Try at beginning of memory
    try:
        # Get two bytes
        memory.read_range(0, 2)
        assert True
    except MemoryOutOfRange:
        assert False

    # Try before valid memory
    try:
        # Get two bytes
        memory.read_range(-1, 1)
        assert False
    except MemoryOutOfRange:
        assert True

    # Try at end of memory
    try:
        memory.read_range(65534, 65536)
        assert True
    except MemoryOutOfRange:
        assert False

    # Try after valid memory
    try:
        memory.read_range(65535, 65537)
        assert False
    except MemoryOutOfRange:
        assert True


def test_memory_memory_dump_default():
    "Test memory_dump with no arguments"
    b = bytes(range(256)) * 10
    m = Memory(b)

    expected_test_result = """0x0000  00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f
0x0010  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f
0x0020  20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f
0x0030  30 31 32 33 34 35 36 37  38 39 3a 3b 3c 3d 3e 3f
0x0040  40 41 42 43 44 45 46 47  48 49 4a 4b 4c 4d 4e 4f
0x0050  50 51 52 53 54 55 56 57  58 59 5a 5b 5c 5d 5e 5f
0x0060  60 61 62 63 64 65 66 67  68 69 6a 6b 6c 6d 6e 6f
0x0070  70 71 72 73 74 75 76 77  78 79 7a 7b 7c 7d 7e 7f
0x0080  80 81 82 83 84 85 86 87  88 89 8a 8b 8c 8d 8e 8f
0x0090  90 91 92 93 94 95 96 97  98 99 9a 9b 9c 9d 9e 9f
0x00a0  a0 a1 a2 a3 a4 a5 a6 a7  a8 a9 aa ab ac ad ae af
0x00b0  b0 b1 b2 b3 b4 b5 b6 b7  b8 b9 ba bb bc bd be bf
0x00c0  c0 c1 c2 c3 c4 c5 c6 c7  c8 c9 ca cb cc cd ce cf
0x00d0  d0 d1 d2 d3 d4 d5 d6 d7  d8 d9 da db dc dd de df
0x00e0  e0 e1 e2 e3 e4 e5 e6 e7  e8 e9 ea eb ec ed ee ef
0x00f0  f0 f1 f2 f3 f4 f5 f6 f7  f8 f9 fa fb fc fd fe ff"""

    assert expected_test_result == m.memory_range_dump()


def test_memory_memory_range_dump_specified_range():
    "Test memory_range_dump with a specified range"
    b = bytes(range(256)) * 10
    m = Memory(b)

    expected_test_result = """0x0000  00 01 02 03 04 05 06 07  08 09 0a 0b 0c 0d 0e 0f
0x0010  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f"""

    assert expected_test_result == m.memory_range_dump(range(0x00, 0x20))


def test_memory_memory_range_dump_specified_range_not_at_start():
    "Test memory_range_dump with a specified range starting at a non-zero location"
    b = bytes(range(256)) * 10
    m = Memory(b)

    expected_test_result = """0x0010  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f
0x0020  20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f"""

    assert expected_test_result == m.memory_range_dump(range(0x10, 0x30))


def test_memory_memory_range_dump_specified_range_non_16_byte_multiple_length():
    """
    Test memory_range_dump with a specified range starting at a non-zero location,
    with non-16-byte multiple length.
    """
    b = bytes(range(256)) * 10
    m = Memory(b)

    expected_test_result = """0x0010  10 11 12 13 14 15 16 17  18 19 1a 1b 1c 1d 1e 1f
0x0020  20 21 22 23 24 25 26 27  28 29 2a 2b 2c 2d 2e 2f"""

    assert expected_test_result == m.memory_range_dump(range(0x10, 0x33))


def test_memory_memory_range_dump_too_small():
    "Test memory_range_dump with a start less than the memory start"
    b = bytes(range(0x20))
    m = Memory(b)

    try:
        m.memory_range_dump(range(-1, 0x20))
        assert False
    except MemoryOutOfRange:
        assert True


def test_memory_memory_range_dump_too_large():
    "Test memory_range_dump with a stop greater than the memory end"
    b = bytes(range(0x20))
    m = Memory(b)

    try:
        m.memory_range_dump(range(0x00, 0x21))
        assert False
    except MemoryOutOfRange:
        assert True
