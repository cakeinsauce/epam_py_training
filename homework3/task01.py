import functools
from collections.abc import Callable


def cache(times: int) -> Callable:
    """Decorator with its maxsize cache."""

    def cacheable_func(func: Callable) -> Callable:
        @functools.lru_cache(maxsize=times)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return cacheable_func
