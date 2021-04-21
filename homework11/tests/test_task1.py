from hw1 import SimplifiedEnum


def test_simplified_class():
    # Testing Enum class without duplicates.
    class SizesEnum(metaclass=SimplifiedEnum):
        __keys = ("XL", "L", "M", "S", "XS")

    assert SizesEnum.XL == "XL"


def test_wrong_syntax_for_simplified_class(capsys):
    # Testing Enum class with wrong key for attrs.
    class ColorsEnum(metaclass=SimplifiedEnum):
        __wrong = ("RED", "BLUE", "ORANGE", "BLACK")

    captured = capsys.readouterr()
    assert captured.err == "No such attribute for enum, try __keys = (*values)\n"
