import pytest
from hw1 import find_occurrences

example_tree = {
    "first": ["RED", "BLUE"],
    "second": {
        "simple_key": ["simple", "list", "of", "RED", "valued"],
    },
    "third": {
        "abc": "BLUE",
        "jhl": "RED",
        "complex_key": {
            "key1": "value1",
            "key2": "RED",
            "key3": ["a", "lot", "of", "values", {"nested_key": "RED"}],
        },
    },
    "fourth": "RED",
}


def test_example_tree_red():
    # Testing find_occurrences to find RED in the tree.
    assert find_occurrences(example_tree, "RED") == 6


def test_empty_tree():
    # Testing empty tree search.
    assert find_occurrences({}, "smth") == 0


def test_tree_key_equals_search_item():
    # Testing tree when key equals to searching item.
    assert find_occurrences({"red": 1, "blue": "red", 3: "red"}, "red") == 2
