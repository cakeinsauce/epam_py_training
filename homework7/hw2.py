"""
Given two strings. Return if they are equal when both are typed into
empty text editors. # means a backspace character.

Note that after backspacing an empty text, the text will continue empty.

Examples:
    Input: s = "ab#c", t = "ad#c"
    Output: True
    # Both s and t become "ac".

    Input: s = "a##c", t = "#a#c"
    Output: True
    Explanation: Both s and t become "c".

    Input: a = "a#c", t = "b"
    Output: False
    Explanation: s becomes "c" while t becomes "b".

"""
from itertools import zip_longest


def backspace_compare(first: str, second: str):
    """Return True if two strings are equal considering backspace character."""

    def string_reduce(string: str):
        skip = False
        for char in reversed(string):
            if char == "#":
                skip = True
            elif skip:
                skip = False
            else:
                yield char

    return all(
        f == s for f, s in zip_longest(string_reduce(first), string_reduce(second))
    )
