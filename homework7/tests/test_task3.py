from typing import List

import pytest
from hw3 import tic_tac_toe_checker


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        [[["-", "-", "o"], ["-", "o", "o"], ["x", "x", "x"]], "x wins!"],
        [[["-", "-", "o"], ["-", "o", "x"], ["o", "x", "x"]], "o wins!"],
        [[["o", "-", "x"], ["o", "o", "-"], ["o", "x", "x"]], "o wins!"],
    ],
)
def test_game_winner(value: List[List], expected_value: str):
    # Testing the winner of the game.
    actual_result = tic_tac_toe_checker(value)

    assert actual_result == expected_value


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        [[["o", "x", "o"], ["x", "o", "o"], ["x", "o", "x"]], "draw!"],
    ],
)
def test_draw(value: List[List], expected_value: str):
    # Testing a draw of the game.
    actual_result = tic_tac_toe_checker(value)

    assert actual_result == expected_value


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        [[["-", "-", "o"], ["x", "o", "o"], ["x", "o", "x"]], "unfinished!"],
    ],
)
def test_unfinished(value: List[List], expected_value: str):
    # Testing the unfinished game.
    actual_result = tic_tac_toe_checker(value)

    assert actual_result == expected_value
