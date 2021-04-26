import datetime as dt
from collections import defaultdict

from django.db import models


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


class Person(models.Model):
    """Person class contains name of a person."""

    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)


class Student(Person):
    """Student class contains student methods for homework."""

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def do_homework(self, homework: "Homework", solution: str):
        if not homework.is_active():
            raise DeadlineError(homework)
        return HomeworkResult(homework, self, solution)


class Teacher(Person):
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


class Homework(models.Model):
    text = models.TextField(blank=True)
    deadline = models.DurationField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def is_active(self) -> bool:
        """Return True if homework is not expired."""
        return dt.datetime.today() < self.created + self.deadline


class HomeworkResult(models.Model):
    homework = models.ForeignKey("Homework", models.PROTECT)
    solution = models.TextField(blank=True)
    author = models.ForeignKey("Student", models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
