from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class CarryFlag(Flag):
    """
    The Carry Flag
    The flag gets set when the result of a compare is zero or positive.
    This flag gets reset when the result of a compare operation is negative.
    """

    def test_result(self, result):
        """
        Test the result
        The flag gets set when the result of a compare is zero or positive.
        This flag gets reset when the result of a compare operation is negative.
        """

        if (result & 0x80) == 0:
            self.set()
        else:
            self.clear()

    def test_register_result(self, register):
        """
        Test the register result
        The flag gets set when the result of a compare is zero or positive.
        This flag gets reset when the result of a compare operation is negative.
        """

        return self.test_result(register.get())
