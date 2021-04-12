from typing import Tuple

import pytest
from oop_1 import *


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [[("HW1", dt.timedelta(days=1)), True], [("HW2", dt.timedelta(days=0)), False]],
)
def test_homework_expiration(value: Tuple[str, dt.timedelta], expected_value: bool):
    # Testing if homework is expired.
    assert Homework(*value).is_active() == expected_value


def test_student_do_homework_expired(capsys):
    # Testing if student has expired his homework.
    hw = Homework("HW1", dt.timedelta(days=0))
    exp_homework = Student.do_homework(hw)
    assert capsys.readouterr().out == "You are late\n" and exp_homework is None


def test_student_do_homework_good_to_do():
    # Testing if student has NOT expired his homework.
    hw = Homework("HW1", dt.timedelta(days=1))
    exp_homework = Student.do_homework(hw)
    assert isinstance(exp_homework, Homework)


def test_create_homework_by_teacher():
    # Testing creating of Homework object by a teacher.
    hw = Teacher.create_homework("HW1", 1)
    assert isinstance(hw, Homework)
