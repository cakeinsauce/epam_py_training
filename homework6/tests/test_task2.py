from unittest.mock import patch

import pytest
from oop_2 import *


def test_homework_result_got_not_homework_instance():
    # Testing IsNotHomeworkInstanceError if HomeworkResult got not Homework instance.
    homework = 1
    student = Student("Denis", "Rybakov")
    with pytest.raises(
        IsNotHomeworkInstanceError,
        match="<class 'int'> --> You gave a not Homework object",
    ):
        HomeworkResult(homework, student, "solution")


def test_student_does_homework_missed_deadline():
    # Testing DeadlineError if Student does homework with missed deadline.
    homework = Homework("Homework", dt.timedelta(days=0))
    student = Student("Denis", "Rybakov")
    with patch.object(DeadlineError, "__str__", return_value="You are late"):
        with pytest.raises(DeadlineError, match="You are late"):
            student.do_homework(homework, "solution")


def test_check_homework_default_dict():
    # Testing homework_done defaultdict with check_homework.
    # Add teachers
    opp_teacher = Teacher("Daniil", "Shadrin")
    advanced_python_teacher = Teacher("Aleksandr", "Smetanin")
    # Add student
    good_student = Student("Lev", "Sokolov")
    # Create homework by the teacher
    oop_hw = opp_teacher.create_homework("Learn OOP", 1)
    # Do homework by the student
    result = good_student.do_homework(oop_hw, "I have done this hw")
    # Check homework by the teacher
    opp_teacher.check_homework(result)
    temp_1 = opp_teacher.homework_done

    advanced_python_teacher.check_homework(result)
    temp_2 = Teacher.homework_done

    assert temp_1 == temp_2


def test_clear_results():
    # Testing reset_results to clear all data from homework_done.
    Teacher.reset_results()
    assert not Teacher.homework_done


def test_pop_homework_result():
    # Testing reset_results to pop certain homework from homework_done.
    # Add students
    good_student = Student("Lev", "Sokolov")
    lazy_student = Student("Roman", "Petrov")
    # Add homework
    docs_hw = Teacher.create_homework("Read docs", 5)
    # Add homework results
    result_1 = good_student.do_homework(docs_hw, "I have done this hw too")
    result_2 = lazy_student.do_homework(docs_hw, "done")
    # Check homework by the teacher
    Teacher.check_homework(result_1)
    Teacher.check_homework(result_2)
    # Delete all docs_hw homework results from dictionary
    Teacher.reset_results(result_1.homework)

    assert not Teacher.homework_done[result_1.homework]
