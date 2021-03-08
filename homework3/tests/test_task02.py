import time

from homework3.task02 import slow_calculate_sum


def test_time_slow_calculate():
    # Time test of slow_calculate_sum.
    start_time = time.perf_counter()
    slow_calculate_sum()
    time_delta = time.perf_counter() - start_time
    assert time_delta < 60
