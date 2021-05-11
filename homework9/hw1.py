"""
Write a function that merges integer from sorted files and returns an iterator

file1.txt:
1
3
5

file2.txt:
2
4
6

>>> list(merge_sorted_files(["file1.txt", "file2.txt"]))
[1, 2, 3, 4, 5, 6]
"""
from pathlib import Path
from typing import Iterator, List, Union


def file_line(file_path: Union[Path, str]) -> Iterator:
    """Yields numbers from the file.

    Args:
        file_path: The path of the file with numbers.

    Yields:
        int: The next number in the file.

    Examples:
        >>> for number in file_line('file1.txt'):
        ...     print(number)
        1
        3
        5

    """
    with open(file_path, "r") as f_o:
        for num in f_o.readlines():
            yield int(num)


def merge_sorted_files(file_list: List[Union[Path, str]]) -> Iterator:
    """Merge integers from sorted files and yields them.

    Args:
        file_list: List of file paths.

    Yields:
        int: The next number from merged integers.

    Examples:
        >>> list(merge_sorted_files(["file1.txt", "file2.txt"]))
        [1, 2, 3, 4, 5, 6]

    """
    f_o1 = file_line(file_list[0])
    f_o2 = file_line(file_list[1])
    num1 = next(f_o1, None)
    num2 = next(f_o2, None)

    while num1 or num2:
        if not num2 or (
            num1 and num1 <= num2
        ):  # Either num1 < num2 and not None, or num2 is None
            yield num1
            num1 = next(f_o1, None)
        else:
            yield num2
            num2 = next(f_o2, None)
