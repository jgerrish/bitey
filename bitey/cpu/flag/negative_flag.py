from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class NegativeFlag(Flag):
    """
    The Negative Flag, also called the N Flag
    Set if the result of an instructions sets bit seven
    """

    def test_register_result(self, register):
        """
        Test the register result
        Set the flag if the result is true
        Reset the flag if the result is not true
        """

        if (register.get() & 0x80) != 0:
            self.status = True
        else:
            self.status = False
