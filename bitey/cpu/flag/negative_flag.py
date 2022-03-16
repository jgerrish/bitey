from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class NegativeFlag(Flag):
    """
    The Negative Flag, also called the N Flag
    Set if the result of an instructions sets bit seven
    """

    def test_result(self, result):
        """
        Test the result
        Set the flag if the result is true
        Reset the flag if the result is not true
        """

        if (result & 0x80) != 0:
            self.set()
        else:
            self.clear()

    def test_register_result(self, register):
        """
        Test the register result
        Set the flag if the result is true
        Reset the flag if the result is not true
        """

        return self.test_result(register.get())
