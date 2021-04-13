from pathlib import Path

from hw3 import universal_file_counter


def test_file_counter_without_tokenizer():
    # Testing counter without tokenizer
    assert universal_file_counter(Path("homework9"), "txt") == 4


def test_file_counter_with_tokenizer():
    # Testing counter with tokenizer
    assert universal_file_counter(Path("homework9"), "txt", str.split) == 4


def test_file_no_files():
    # Testing counter with no files
    assert universal_file_counter(Path("homework9"), "sqlite", str.split) == 0
