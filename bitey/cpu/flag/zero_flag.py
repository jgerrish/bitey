from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class ZeroFlag(Flag):
    """
    The Zero Flag, also called the Zero Result Flag
    """

    def test_register_result(self, register):
        """
        Test the register result
        Set the flag if the result is zero
        Reset the flag if the result is non-zero
        """

        if register == 0:
            self.status = True
        else:
            self.status = False
