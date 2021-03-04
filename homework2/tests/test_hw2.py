from typing import List, Tuple

import pytest
from hw2 import major_and_minor_elem


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        ([3, 2, 3], (3, 2)),
        ([2, 2, 1, 1, 1, 2, 2], (2, 1)),
        ([3, 2, 3, 4, "a", "a", "a", 4, 4, 4, 4, 4, 4], (4, 2)),
        ([1, 1, 1, 1], (1, 1)),
    ],
)
def test_major_and_minor_elem(value: List, expected_value: Tuple[int, int]):
    # The most and the least common elements in a list smoke-test.
    actual_result = major_and_minor_elem(value)

    assert actual_result == expected_value
