from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class ZeroFlag(Flag):
    """
    The Zero Flag, also called the Zero Result Flag
    """

    def test_result(self, result):
        """
        Test the result
        Set the flag if the result is zero
        Reset the flag if the result is non-zero
        """

        if result == 0:
            self.set()
        else:
            self.clear()

    def test_register_result(self, register):
        """
        Test the register result
        Set the flag if the result is zero
        Reset the flag if the result is non-zero
        """

        return self.test_result(register.get())
