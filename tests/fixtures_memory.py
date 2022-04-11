def init_memory(memory, init_list):
    """
    Setup memory for tests
    The first argument is the Memory
    The second argument is a list of 2-tuples
    Each 2-tuple contains an address what value should be stored there
    """
    for item in init_list:
        memory.write(item[0], item[1])
