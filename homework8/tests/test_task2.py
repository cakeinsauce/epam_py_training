import pytest
from task2 import TableData

a = TableData("homework8/example.sqlite", "books")
b = TableData("homework8/example.sqlite", "presidents")


def test_database_len():
    # Testing __len__ implementation.
    assert len(a) == 3


def test_indexing():
    # Testing __getitem__ implementation.
    assert b["Yeltsin"] == ("Yeltsin", 999, "Russia")


def test_indexing_no_such_row():
    # Testing __getitem__ implementation when there's no such row with the given key.
    assert b["Put in"] is None


def test_contains():
    # Testing __contains__ implementation.
    assert ("1984" in a) is True


def test_do_not_contain():
    # Testing __contains__ implementation.
    assert ("Harry Potter" in a) is False


def test_iterating():
    # Testing iteration protocol implementation.
    names = ["Yeltsin", "Trump", "Big Man Tyrone"]
    for name in enumerate(b):
        assert name[1][0] == names[name[0]]
