"""
В этом задании будем улучшать нашу систему классов из задания прошлой лекции
(Student, Teacher, Homework)
Советую обратить внимание на defaultdict из модуля collection для
использования как общую переменную


1. Как то не правильно, что после do_homework мы возвращаем все тот же
объект - будем возвращать какой-то результат работы (HomeworkResult)

HomeworkResult принимает объект автора задания, принимает исходное задание
и его решение в виде строки
Атрибуты:
    homework - для объекта Homework, если передан не этот класс -  выкинуть
    подходящие по смыслу исключение с сообщением:
    'You gave a not Homework object'

    solution - хранит решение ДЗ как строку
    author - хранит объект Student
    created - c точной датой и временем создания

2. Если задание уже просрочено хотелось бы видеть исключение при do_homework,
а не просто принт 'You are late'.
Поднимайте исключение DeadlineError с сообщением 'You are late' вместо print.

3. Student и Teacher имеют одинаковые по смыслу атрибуты
(last_name, first_name) - избавиться от дублирования с помощью наследования

4.
Teacher
Атрибут:
    homework_done - структура с интерфейсом как в словаря, сюда поподают все
    HomeworkResult после успешного прохождения check_homework
    (нужно гаранитровать остутствие повторяющихся результатов по каждому
    заданию), группировать по экземплярам Homework.
    Общий для всех учителей. Вариант ипользования смотри в блоке if __main__...
Методы:
    check_homework - принимает экземпляр HomeworkResult и возвращает True если
    ответ студента больше 5 символов, так же при успешной проверке добавить в
    homework_done.
    Если меньше 5 символов - никуда не добавлять и вернуть False.

    reset_results - если передать экземпряр Homework - удаляет только
    результаты этого задания из homework_done, если ничего не передавать,
    то полностью обнулит homework_done.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""

import datetime as dt
from collections import defaultdict


class IsNotHomeworkInstanceError(Exception):
    """Exception raised for errors in the input homework attribute."""

    def __init__(self, homework: any, message="You gave a not Homework object"):
        self.homework = homework
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{type(self.homework)} --> {self.message}"


class DeadlineError(Exception):
    """Exception raised for missed homework deadline."""

    def __init__(self, homework, message="You are late"):
        self.homework = homework
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return (
            f"Deadline: {self.homework.created + self.homework.deadline}, "
            f"Now: {dt.datetime.today()} --> {self.message}"
        )


class Person:
    """Person class contains name of a person."""

    def __init__(self, last_name: str, first_name: str):
        self.last_name = last_name
        self.first_name = first_name


class Student(Person):
    """Student class contains student methods for homework."""

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def do_homework(self, homework: "Homework", solution: str) -> "HomeworkResult":
        """Return HomeworkResult object if it's not expired yet otherwise, DeadlineError is raised."""
        if not homework.is_active():
            raise DeadlineError(homework)
        return HomeworkResult(homework, self, solution)


class Teacher(Person):
    """Teacher class contains teacher methods for homework."""

    homework_done = defaultdict(list)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @staticmethod
    def create_homework(text: str, days: int):
        """Return created Homework object."""
        return Homework(text, dt.timedelta(days=days))

    @staticmethod
    def check_homework(homework_result: "HomeworkResult") -> bool:
        """Return True if homework solution is more than 5 characters and
        add homework_result to homework_done otherwise just return False."""

        if len(homework_result.solution) <= 5:
            return False

        Teacher.homework_done[homework_result.homework].append(
            homework_result
        )  # Add homework result to done homeworks, group by Homework instance.
        return True

    @staticmethod
    def reset_results(homework=None):
        """If homework is None, clear homework_done dict otherwise, remove homework's results."""
        if homework is None:
            Teacher.homework_done.clear()
        else:
            Teacher.homework_done[homework] = []


class Homework:
    """Homework class contains attributes about a homework."""

    def __init__(self, text: str, deadline: dt.timedelta):
        self.text = text
        self.deadline = deadline
        self.created = dt.datetime.today()

    def __str__(self):
        return self.text

    def is_active(self) -> bool:
        """Return True if homework is not expired."""
        return dt.datetime.today() < self.created + self.deadline


class HomeworkResult:
    """HomeworkResult contains done homeworks."""

    def __init__(self, homework: Homework, author: "Student", solution: str):
        if not isinstance(homework, Homework):
            raise IsNotHomeworkInstanceError(homework)
        self.homework = homework
        self.solution = solution
        self.author = author
        self.created = dt.datetime.today()


# if __name__ == "__main__":
#     opp_teacher = Teacher("Daniil", "Shadrin")
#     advanced_python_teacher = Teacher("Aleksandr", "Smetanin")
#
#     lazy_student = Student("Roman", "Petrov")
#     good_student = Student("Lev", "Sokolov")
#
#     oop_hw = opp_teacher.create_homework("Learn OOP", 1)
#     docs_hw = opp_teacher.create_homework("Read docs", 5)
#
#     result_1 = good_student.do_homework(oop_hw, "I have done this hw")
#     result_2 = good_student.do_homework(docs_hw, "I have done this hw too")
#     result_3 = lazy_student.do_homework(docs_hw, "done")
#     try:
#         result_4 = HomeworkResult(good_student, "fff", "Solution")
#     except Exception:
#         print("There was an exception here")
#     opp_teacher.check_homework(result_1)
#     temp_1 = opp_teacher.homework_done
#
#     advanced_python_teacher.check_homework(result_1)
#     temp_2 = Teacher.homework_done
#     assert temp_1 == temp_2
#
#     opp_teacher.check_homework(result_2)
#     opp_teacher.check_homework(result_3)
#
#     print(Teacher.homework_done[oop_hw])
#     Teacher.reset_results()
