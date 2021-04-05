import pytest
from task1 import KeyValueStorage


@pytest.fixture(autouse=True)
def write_to_file():
    with open("homework8/task1.txt", "w") as f_o:
        txt = "name=kek\nlast_name=top\npower=9001\nsong=shadilay"
        f_o.write(txt)


def test_dot_access():
    # Testing dot access to attributes.
    storage = KeyValueStorage("homework8/task1.txt")
    assert storage.name == "kek"


def test_index_access():
    # Testing indexing.
    storage = KeyValueStorage("homework8/task1.txt")
    assert storage["power"] == 9001


def test_built_in_not_override():
    # Testing that built-in attributes are not override.
    with open("homework8/task1.txt", "a") as f_o:
        f_o.write("\n__dict__=1")
    storage = KeyValueStorage("homework8/task1.txt")

    assert "last_name" in storage.__dict__


def test_value_error_digit_key():
    # Testing ValueError raises if key is a number.
    with open("homework8/task1.txt", "a") as f_o:
        f_o.write("\n1=something")

    with pytest.raises(ValueError):
        KeyValueStorage("homework8/task1.txt")
