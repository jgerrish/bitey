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
