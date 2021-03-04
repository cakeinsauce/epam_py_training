"""
Given a file containing text. Complete using only default collections:
    1) Find 10 longest words consisting of largest amount of unique symbols
    2) Find rarest symbol for the document
    3) Count every punctuation char
    4) Count every non-ascii char
    5) Find most common non-ascii char for the document
"""
from collections import Counter
from string import punctuation
from typing import List

# All functions have been written to work with the given text.


def get_file_data(file_path: str) -> str:
    """Return encoded unicode-escaped text."""
    with open(file_path, "r", encoding="unicode_escape") as f_o:
        return f_o.read()


def get_longest_diverse_words(file_path: str) -> List[str]:
    """Return list of 10 longest words consisting of largest amount of unique symbols."""
    # Consider that word consists only of alphabetical characters and separated by punctuation marks or spaces.
    words_length = []
    uniq_words = set(
        "".join(
            [c for c in get_file_data(file_path) if c.isalpha() or c.isspace()]
        ).split()
    )  # Create list only with letters and spaces -> Create string out of it ->
    # -> Split into words -> Create set with unique words.

    for (
        word
    ) in uniq_words:  # Create list with tuples of word and its unique symbols' amount.
        uniq_sym_amount = len(set(word.lower()))
        words_length.append((uniq_sym_amount, word))

    diverse_words = [
        word[1] for word in sorted(words_length)[:-11:-1]
    ]  # Get obtained words from tuples.
    return diverse_words


def get_rarest_char(file_path: str) -> str:
    """Return rarest symbol for a document."""
    alphanum_text = [
        c.lower() for c in get_file_data(file_path) if c.isalnum()
    ]  # Create list only with letters and numbers
    return Counter(alphanum_text).most_common()[-1][
        0
    ]  # Get last tuple and its 1st element that is a letter


def count_punctuation_chars(file_path: str) -> int:
    """Return every punctuation char's amount."""
    amount = 0
    for c in get_file_data(file_path):
        if c in punctuation:
            amount += 1
    return amount


def count_non_ascii_chars(file_path: str) -> int:
    """Return every non-ascii char's amount."""
    amount = 0
    for c in get_file_data(file_path):
        if not c.isascii():
            amount += 1
    return amount


def get_most_common_non_ascii_char(file_path: str) -> str:
    """Return most common non-ascii char for a document"""
    non_ascii_text = [
        c.lower() for c in get_file_data(file_path) if not c.isascii()
    ]  # Create list only with non-ascii chars
    return Counter(non_ascii_text).most_common()[0][
        0
    ]  # Get 1st tuple and its 1st element that is a letter
