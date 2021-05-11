import pytest
from hw2 import Suppressor, suppressor


def test_context_manager_generator():
    # Testing suppression of the given exception by generator
    with suppressor(IndexError):
        [][2]


def test_context_manager_generator_different_exception():
    # Testing suppression when different exception's given.
    with pytest.raises(NameError):
        with suppressor(IndexError):
            name


def test_context_manager_class():
    # Testing suppression of the given exception by class
    with Suppressor(IndexError):
        [][2]


def test_context_manager_class_different_exception():
    # Testing suppression of the given exception by class
    with pytest.raises(NameError):
        with Suppressor(IndexError):
            name
