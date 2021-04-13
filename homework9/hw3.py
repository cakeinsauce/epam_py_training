"""
Write a function that takes directory path, a file extension and an optional tokenizer.
It will count lines in all files with that extension if there are no tokenizer.
If a the tokenizer is not none, it will count tokens.

For dir with two files from hw1.py:
>>> universal_file_counter(test_dir, "txt")
6
>>> universal_file_counter(test_dir, "txt", str.split)
6

"""
import os
from pathlib import Path
from typing import Callable, Optional


def universal_file_counter(
    dir_path: Path, file_extension: str, tokenizer: Optional[Callable] = None
) -> int:
    counter = 0
    files_paths = []

    for file in os.listdir(
        dir_path
    ):  # Creating list of files paths with the given extension.
        if file.endswith("." + file_extension):
            files_paths.append(dir_path.joinpath(file))

    for path in files_paths:
        with open(path, "r") as f_o:
            for line in f_o:  # Parsing all lines in a file.
                if tokenizer:
                    counter += len(list(map(tokenizer, (line,))))
                elif line != "\n":
                    counter += 1

    return counter
