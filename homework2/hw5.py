"""
Some of the functions have a bit cumbersome behavior when we deal with
positional and keyword arguments.

Write a function that accept any iterable of unique values and then
it behaves as range function:


import string


assert = custom_range(string.ascii_lowercase, 'g') == ['a', 'b', 'c', 'd', 'e', 'f']
assert = custom_range(string.ascii_lowercase, 'g', 'p') == ['g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o']
assert = custom_range(string.ascii_lowercase, 'p', 'g', -2) == ['p', 'n', 'l', 'j', 'h']

"""
from collections.abc import Hashable, Iterable
from typing import List


def custom_range(iter_seq: Iterable, *args: Hashable) -> List[Hashable]:
    """Implement range-like function for any iterable object."""
    step = 1
    start = None

    args_amt = len(args)

    if args_amt == 1:  # One positional argument to function (stop)
        stop = args[0]
    elif args_amt > 1:  # Two positional arguments to function (start, stop)
        start = args[0]
        stop = args[1]
        if args_amt == 3:  # Three positional arguments to function (start, stop, step)
            step = args[2]

    slicing_start = None
    slicing_end = None

    for i, v in enumerate(iter_seq):  # Iterate over sequence
        if start == v:  # Set start slicing index
            slicing_start = i
        if stop == v:  # Set stop slicing index
            slicing_end = i
        if slicing_end and (
            not start or slicing_start
        ):  # End cycle if stop or start and stop have found.
            break

    return list(iter_seq)[slicing_start:slicing_end:step]
