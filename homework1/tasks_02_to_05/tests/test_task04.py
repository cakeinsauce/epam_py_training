import time
from typing import List, Tuple

import pytest
from tasks_02_to_05.task04 import check_sum_of_four


def create_lists(length=100):
    a = [1 for _ in range(length)]
    b = list(a)
    c = [-1 for _ in range(10000)]
    d = list(c)
    return a, b, c, d


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (([1, 2], [-2, -1], [-1, 2], [0, 2]), 2),
        (([0, 0], [0, 0], [0, 0], [0, 0]), 16),
        (([0, 1], [0, 0], [0, 0], [-1, 0]), 8),
        (([12, 15], [-12, 15], [-15, -12], [12, -30]), 2),
    ],
)
def test_check_sum_of_four_smoke(
    value: Tuple[List[int], List[int], List[int], List[int]], expected_result: int
):
    # Simple smoke-test
    actual_result = check_sum_of_four(*value)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (100, 100 ** 4),
        (1000, 1000 ** 4),
        (10000, 10000 ** 4),
    ],
)
def test_check_sum_of_four_stress(value: int, expected_result: int):
    # Large list stress-test
    start_time = time.time()
    actual_result = check_sum_of_four(*create_lists(value))
    print(" Exec time: {!s}s".format(time.time() - start_time))
    assert actual_result == expected_result
