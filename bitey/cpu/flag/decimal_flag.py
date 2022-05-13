from dataclasses import dataclass
from bitey.cpu.flag.flag import Flag


@dataclass
class DecimalFlag(Flag):
    """
    The Decimal Flag

    Set to enable decimal arithmetic mode
    Clear to enable normal binary arithmetic mode
    """
