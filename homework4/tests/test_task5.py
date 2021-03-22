from typing import List

import pytest
from task_5_optional import fizzbuzz


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (5, ["1", "2", "fizz", "4", "buzz"]),
        (0, []),
        (-1, []),
    ],
)
def test_fizzbuzz_generator(value: int, expected_value: List[str]):
    # Positive test fizzbuzz generator
    fizzbuzz_gen = fizzbuzz(value)
    for actual_result in enumerate(fizzbuzz_gen):
        assert expected_value[actual_result[0]] == actual_result[1]
