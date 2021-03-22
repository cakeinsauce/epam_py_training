"""
Необходимо создать 3 класса и взаимосвязь между ними (Student, Teacher,
Homework)
Наследование в этой задаче использовать не нужно.
Для работы с временем использовать модуль datetime

1. Homework принимает на вход 2 атрибута: текст задания и количество дней
на это задание
Атрибуты:
    text - текст задания
    deadline - хранит объект datetime.timedelta с количеством
    дней на выполнение
    created - c точной датой и временем создания
Методы:
    is_active - проверяет не истело ли время на выполнение задания,
    возвращает boolean

2. Student
Атрибуты:
    last_name
    first_name
Методы:
    do_homework - принимает объект Homework и возвращает его же,
    если задание уже просрочено, то печатет 'You are late' и возвращает None

3. Teacher
Атрибуты:
     last_name
     first_name
Методы:
    create_homework - текст задания и количество дней на это задание,
    возвращает экземпляр Homework
    Обратите внимание, что для работы этого метода не требуется сам объект.

PEP8 соблюдать строго.
Всем перечисленным выше атрибутам и методам классов сохранить названия.
К названием остальных переменных, классов и тд. подходить ответственно -
давать логичные подходящие имена.
"""
import datetime as dt
from typing import Union


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


class Student:
    """Student class contains info about a student."""

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @staticmethod
    def do_homework(homework: Homework) -> Union[Homework, None]:
        """Return Homework object if it's not expired yet otherwise, None."""
        if homework.is_active():
            return homework
        else:
            print("You are late")
            return None


class Teacher:
    """Teacher class contains info about a teacher."""

    def __init__(self, last_name, first_name):
        self.last_name = last_name
        self.first_name = first_name

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @staticmethod
    def create_homework(text, days):
        """Return created Homework object."""
        return Homework(text, dt.timedelta(days=days))


if __name__ == "__main__":
    teacher = Teacher("Daniil", "Shadrin")
    student = Student("Roman", "Petrov")
    teacher.last_name  # Daniil
    student.first_name  # Petrov

    expired_homework = teacher.create_homework("Learn functions", 0)
    expired_homework.created  # Example: 2019-05-26 16:44:30.688762
    expired_homework.deadline  # 0:00:00
    expired_homework.text  # 'Learn functions'

    # create function from method and use it
    create_homework_too = teacher.create_homework
    oop_homework = create_homework_too("create 2 simple classes", 5)
    oop_homework.deadline  # 5 days, 0:00:00

    student.do_homework(oop_homework)
    student.do_homework(expired_homework)  # You are late
