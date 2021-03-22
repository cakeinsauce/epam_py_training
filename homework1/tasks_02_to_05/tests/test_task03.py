import random
from typing import Tuple

import pytest
from tasks_02_to_05.task03 import find_maximum_and_minimum


def create_test_data(min_v, max_v, length=10, file="test_min_max_file.txt"):
    values = [random.randint(min_v, max_v) for _ in range(length - 2)]
    values.extend([min_v, max_v])
    random.shuffle(values)

    with open(file, "w") as t_d:
        t_d.writelines("\n".join(map(str, values)))


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        ((10, 20), (10, 20)),
        ((8, 13, 100), (8, 13)),
        ((-10, 20), (-10, 20)),
        ((-5, -5), (-5, -5)),
        ((15, 15), (15, 15)),
        ((0, 0), (0, 0)),
    ],
)
def test_find_maximum_and_minimum(
    value: Tuple[int, int], expected_result: Tuple[int, int]
):
    # Simple smoke-test
    create_test_data(*value)
    actual_result = find_maximum_and_minimum("test_min_max_file.txt")

    assert actual_result == expected_result
