import os
from numbers import Number

import pytest
from task_1_read_file import read_magic_number


@pytest.fixture
def file_write():

    created_file = []

    def _file_write(data):  # Creating .txt file with data in it.
        with open("tmp.txt", "w") as f_tmp:
            f_tmp.write(str(data))
            f_path = os.path.realpath(f_tmp.name)
            created_file.append(f_path)
        return f_path

    yield _file_write

    os.remove(created_file[0])  # Delete all created files.


@pytest.mark.parametrize(
    "value",
    [
        1,
        1.0,
        2,
        2.9,
    ],
)
def test_is_magic_number(value: Number, file_write):
    # Positive test of magic number that is in [1, 3).
    assert read_magic_number(file_write(value)) is True


@pytest.mark.parametrize("value", [0, 0.99, 3, 4])
def test_is_not_magic_number(value: Number, file_write):
    # Positive test of magic number that is not in [1, 3).
    assert read_magic_number(file_write(value)) is False


@pytest.mark.parametrize("value", ["asd", None, -1])
def test_invalid_file_path(value: str):
    # Negative test invalid path name.
    with pytest.raises(FileNotFoundError):
        read_magic_number(value)


@pytest.mark.parametrize("value", ["..", "aaaa", "1..0"])
def test_invalid_data(value: Number, file_write):
    # Negative test not numeric/ValueError.
    with pytest.raises(ValueError):
        read_magic_number(file_write(value))
