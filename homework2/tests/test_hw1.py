import os
from typing import List

import pytest
from hw1 import *

data_test = os.path.join(os.path.dirname(__file__), "data_test.txt")
data_test2 = os.path.join(os.path.dirname(__file__), "data_test2.txt")


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (
            data_test,
            [
                "überwältigende",
                "heitsvorstellungen",
                "unsichtbaren",
                "überraschenden",
                "festzuhalten",
                "Übermacht",
                "Waldgänger",
                "Gewaltanwendung",
                "zubilligen",
                "heraustreten",
            ],
        ),
    ],
)
def test_get_longest_diverse_words(value: str, expected_result: List[str]):
    # Getting 10 longest diverse words in a text smoke-test
    actual_result = get_longest_diverse_words(value)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (data_test, "p"),
        (data_test2, "3"),
    ],
)
def test_get_rarest_char(value: str, expected_result: str):
    # Getting rarest symbol in a text smoke-test
    actual_result = get_rarest_char(value)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (data_test, 45),
        (data_test2, 9),
    ],
)
def test_count_punctuation_chars(value: str, expected_result: int):
    # Getting amount of punctuation chars smoke-test
    actual_result = count_punctuation_chars(value)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (data_test, 25),
        (data_test2, 0),
    ],
)
def test_count_non_ascii_chars(value: str, expected_result: int):
    # Getting amount of non-ascii chars smoke-test
    actual_result = count_non_ascii_chars(value)

    assert actual_result == expected_result


@pytest.mark.parametrize(
    ["value", "expected_result"],
    [
        (data_test, "ß"),
    ],
)
def test_get_most_common_non_ascii_char(value: str, expected_result: str):
    # Getting most common non-ascii char smoke-test
    actual_result = get_most_common_non_ascii_char(value)

    assert actual_result == expected_result
