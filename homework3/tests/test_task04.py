import pytest

from homework3.task04 import is_armstrong


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (0, True),
        (1, True),
        (9, True),
        (153, True),
        (548834, True),
        (10, False),
        (-1, False),
        (-9, False),
        (-9, False),
        (-153, False),
    ],
)
def test_is_armstrong(value: int, expected_value: bool):
    # Testing is_armstrong number.
    actual_result = is_armstrong(value)

    assert actual_result == expected_value
