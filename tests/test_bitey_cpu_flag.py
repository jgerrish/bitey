from bitey.cpu.flag.flag import Flag, Flags, FlagsJSONDecoder


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


def test_cpu_flags_json_decoder():
    s = '''
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
    '''
    f = FlagsJSONDecoder()
    flags = f.decode(s)
    assert len(flags.flags) == 2
