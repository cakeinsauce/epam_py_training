"""
Vasya implemented nonoptimal Enum classes.
Remove duplicates in variables declarations using metaclasses.

from enum import Enum


class ColorsEnum(Enum):
    RED = "RED"
    BLUE = "BLUE"
    ORANGE = "ORANGE"
    BLACK = "BLACK"


class SizesEnum(Enum):
    XL = "XL"
    L = "L"
    M = "M"
    S = "S"
    XS = "XS"


Should become:

class ColorsEnum(metaclass=SimplifiedEnum):
    __keys = ("RED", "BLUE", "ORANGE", "BLACK")


class SizesEnum(metaclass=SimplifiedEnum):
    __keys = ("XL", "L", "M", "S", "XS")


assert ColorsEnum.RED == "RED"
assert SizesEnum.XL == "XL"
"""
import sys


class SimplifiedEnum(type):
    """Metaclass to simplify duplicates in variables declaration for Enum classes"""

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        try:
            for item in attrs[f"_{name}__keys"]:
                setattr(cls, item, item)
        except KeyError:
            print("No such attribute for enum, try __keys = (*values)", file=sys.stderr)
        return cls
