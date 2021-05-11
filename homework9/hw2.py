"""
Write a context manager, that suppresses passed exception.
Do it both ways: as a class and as a generator.

>>> with suppressor(IndexError):
...    [][2]

"""
from contextlib import contextmanager, suppress


@contextmanager
def suppressor(*exceptions):
    """Context manager that suppresses passed exceptions

    Args:
        *exceptions: Exceptions to suppress.

    Yields:
        None: Yields nothing

    Examples:
        >>> with suppressor(IndexError):
        ...     [][2]

    """
    with suppress(*exceptions):
        yield


class Suppressor:
    """Context manager that suppresses passed exceptions

    Examples:
        >>> with Suppressor(NameError):
        ...     abc

    """

    def __init__(self, *exceptions):
        """Initializing exceptions to suppress.

        Args:
            *exceptions: Exceptions to suppress.

        """
        self.exceptions = exceptions

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if issubclass(exc_type, self.exceptions):
            return True
