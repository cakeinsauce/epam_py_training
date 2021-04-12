import os

import pytest
from hw1 import merge_sorted_files


@pytest.fixture(autouse=True)
def file_delete():
    yield
    if os.path.exists("file1.txt"):
        os.remove("file1.txt")
    if os.path.exists("file2.txt"):
        os.remove("file2.txt")


def test_merge_sorted_files():
    # Merge integers from two files
    with open("file1.txt", "w") as f1, open("file2.txt", "w") as f2:
        f1.write("1\n3\n5")
        f2.write("2\n4\n6")

    assert list(merge_sorted_files(["file1.txt", "file2.txt"])) == [1, 2, 3, 4, 5, 6]


def test_empty_files():
    # Merge empty files
    with open("file1.txt", "w") as f1, open("file2.txt", "w") as f2:
        f1.write("")
        f2.write("")

    assert list(merge_sorted_files(["file1.txt", "file2.txt"])) == []
