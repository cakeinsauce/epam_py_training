import string
from collections.abc import Hashable, Iterable
from typing import List, Optional, Tuple

import pytest
from hw5 import custom_range


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        ((string.ascii_lowercase, "g"), ["a", "b", "c", "d", "e", "f"]),
        (
            (string.ascii_lowercase, "g", "p"),
            ["g", "h", "i", "j", "k", "l", "m", "n", "o"],
        ),
        ((string.ascii_lowercase, "p", "g", -2), ["p", "n", "l", "j", "h"]),
        (([1, 13, 4, 5, 7, 9, 12], 4, 7), [4, 5]),
        (([1, 13, 4, 5, 7, 9, 12], 9, 4, -3), [9]),
        (([1], 1), []),
        (([1, 2], 2), [1]),
    ],
)
def test_custom_range(
    value: Tuple[Iterable, Tuple[any]],
    expected_value: List[Hashable],
):
    # Custom range smoke-test.
    actual_result = custom_range(*value)

    assert actual_result == expected_value
