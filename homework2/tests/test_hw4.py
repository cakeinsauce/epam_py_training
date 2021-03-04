import time
from collections import Callable
from typing import Tuple

import pytest
from hw4 import cache


def func(a, b):
    return (a ** b) ** 2


cache_func = cache(func)


@pytest.mark.parametrize(
    "value",
    [
        (100, 200000),
        (100, 400000),
    ],
)
def test_cache(value: Tuple):
    # Cache function's call smoke-test
    first_time = time.time()
    actual_result = cache_func(*value)
    print("\nFirst call: {:s}".format(str(time.time() - first_time)))
    second_time = time.time()
    expected_result = cache_func(*value)
    print("Second call: {:s}".format(str(time.time() - second_time)))

    assert actual_result is expected_result
