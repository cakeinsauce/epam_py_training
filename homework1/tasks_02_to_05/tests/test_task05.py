from typing import List, Tuple

import pytest
from tasks_02_to_05.task05 import find_maximal_subarray_sum


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (([-2, -5, 6, -2, -3, 1, 5, -6], 5), 7),
        (([1, 3, -1, -3, 5, 3, 6, 7], 3), 16),
        (([-2, -5, 6], 4), -1),
        (([0, 0, 0, 0, 0], 3), 0),
    ],
)
def test_find_maximal_subarray_sum(value: Tuple[List[int], int], expected_result: int):
    # Simple smoke-test finding sub-array sum
    actual_result = find_maximal_subarray_sum(*value)

    assert actual_result == expected_result
