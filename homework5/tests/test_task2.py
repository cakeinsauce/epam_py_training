import pytest
from save_original_info import *

custom_sum(1, 2, 3, 4)


def test_saved_wrapped_func_name():
    # Testing saved original wrapped function name
    assert custom_sum.__name__ == "custom_sum"


def test_saved_wrapped_func_doc():
    # Testing saved original wrapped function docstring
    assert custom_sum.__doc__ == "This function can sum any objects which have __add___"


def test_saved_wrapped_func_object(capsys):
    # Testing saved original wrapped function object
    without_print = custom_sum.__original_func
    without_print(1, 2, 3, 4)

    assert capsys.readouterr().out == ""
