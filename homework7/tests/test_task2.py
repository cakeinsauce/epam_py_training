from typing import Tuple

import pytest
from hw2 import backspace_compare


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (("ab#c", "ad#c"), True),
        (("a##c", "#a#c"), True),
    ],
)
def test_strings_equal(value: Tuple[str, str], expected_value: bool):
    # Testing when two strings are equal and not empty.
    actual_result = backspace_compare(*value)

    assert actual_result == expected_value


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (("a#c", "b"), False),
        (("a##c", "#ac"), False),
    ],
)
def test_strings_not_equal(value: Tuple[str, str], expected_value: bool):
    # Testing when two strings are equal and not empty.
    actual_result = backspace_compare(*value)

    assert actual_result == expected_value


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (("", ""), True),
        (("##", ""), True),
        (("##", "###"), True),
    ],
)
def test_empty_strings(value: Tuple[str, str], expected_value: bool):
    # Testing when two strings are empty.
    actual_result = backspace_compare(*value)

    assert actual_result == expected_value
