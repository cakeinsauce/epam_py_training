"""
Here's a not very efficient calculation function that calculates something important.

Calculate total sum of slow_calculate() of all numbers starting from 0 to 500.
Calculation time should not take more than a minute. Use functional capabilities of multiprocessing module.
You are not allowed to modify slow_calculate function.
"""

import hashlib
import multiprocessing
import random
import struct
import time


def slow_calculate(value):
    """Some weird voodoo magic calculations"""
    time.sleep(random.randint(1, 3))
    data = hashlib.md5(str(value).encode()).digest()
    return sum(struct.unpack("<" + "B" * len(data), data))


def slow_calculate_sum(pool_size: int = 50) -> int:
    """Return sum of slow_calculate of all numbers from 0 to 500."""
    with multiprocessing.Pool(pool_size) as executor:
        return sum(executor.map(slow_calculate, range(501)))
