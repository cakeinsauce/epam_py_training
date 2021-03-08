import functools
from collections.abc import Callable


def cache(func: Callable) -> Callable:
    """Return cached function's call."""

    @functools.lru_cache
    def cacheable_func(*args, **kwargs):
        func(*args, **kwargs)

    return cacheable_func
