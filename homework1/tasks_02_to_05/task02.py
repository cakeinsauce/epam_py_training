"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fibonacci", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence
We guarantee, that the given sequence contains >= 0 integers inside.
"""
from typing import Sequence


def is_perfect_square(n: int) -> bool:
    """Return true if n is a perfect square."""
    return int(n ** 0.5) ** 2 == n


def is_fibonacci_number(n: int) -> bool:
    """Return true if n is a fibonacci number"""
    return is_perfect_square(5 * n ** 2 + 4) or is_perfect_square(5 * n ** 2 - 4)


def check_fibonacci(data: Sequence[int]) -> bool:
    """Return true if data is a fibonacci sequence."""
    golden_ratio = (
        1 + 5 ** 0.5
    ) / 2  # The ratio of two adjacent numbers in Fib sequence approaches Golden Ratio.
    seq_len = len(data)
    start_point = 0
    if not data:  # Zero-length sequence
        return False
    elif seq_len == 1 or not is_fibonacci_number(
        data[0]
    ):  # Either unary-length sequence, or first number is not Fib number.
        return is_fibonacci_number(data[0])

    if data[0] == 0:
        if data[1] == 0:  # Sequence starts with 0, 0
            return False
        elif data[1] == 1:  # Sequence starts with 0, 1
            start_point = 2
    elif data[:2] == [1, 1]:  # Sequence starts with 1, 1
        start_point = 1

    for n in range(start_point, seq_len - 1):
        if not round(data[n] * golden_ratio) == data[n + 1]:
            return False
    return True
