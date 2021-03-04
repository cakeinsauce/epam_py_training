from typing import Any, List

import pytest
from hw3 import combinations


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (
            [[1, 2], [3, 4]],
            [
                [1, 3],
                [1, 4],
                [2, 3],
                [2, 4],
            ],
        ),
        (
            [[1], [3]],
            [
                [1, 3],
            ],
        ),
        (
            [[1, 2], ["a", "b"]],
            [
                [1, "a"],
                [1, "b"],
                [2, "a"],
                [2, "b"],
            ],
        ),
    ],
)
def test_combinations(value: List[any], expected_result: List[List]):
    # List of combination of all lists smoke-test
    actual_result = combinations(*value)

    assert actual_result == expected_result
