import time

import pytest

from homework3.task01 import cache


@cache(times=2)
def fun(a, b):
    return (a ** b) ** 2


@pytest.mark.parametrize(
    "value",
    [
        (100, 40000),
    ],
)
def test_cache(value: int):
    # Cache decorator with cache's maxsize arg test.
    first_time = time.time()
    actual_result = fun(*value)
    print("\nFirst call: {:s}".format(str(time.time() - first_time)))
    second_time = time.time()
    expected_result = fun(*value)
    print("Second call: {:s}".format(str(time.time() - second_time)))
    assert actual_result is expected_result
