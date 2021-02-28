from typing import Sequence

import pytest
from tasks_02_to_05.task02 import check_fibonacci


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        ([], False),
        ([0], True),
        ([1], True),
        ([4], False),
        ([0, 0], False),  ### 4
        ([0, 1], True),
        ([0, 3], False),
        ([1, 1], True),
        ([4, 0], False),
        ([0, 1, 1], True),
        ([1, 1, 1], False),
        ([1, 2, 3], True),
        ([34, 55, 89], True),
        ([0, 0, 0, 1], False),
        ([5, 8, 13, 22], False),
        ([2, 3, 5, 0, 1, 1], False),
        ([0, 1, 1, 2, 3, 5, 8, 13, 21], True),
        ([55, 89, 144, 233, 377, 610], True),
    ],
)
def test_fibonacci(value: Sequence[int], expected_result: bool):
    actual_result = check_fibonacci(value)

    assert actual_result == expected_result
