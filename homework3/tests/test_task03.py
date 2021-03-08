from typing import Dict, List

import pytest

from homework3.task03 import Filter, make_filter, sample_data


def get_even_number(rng=100):
    return [n for n in range(1, rng) if not n % 2 and isinstance(n, int)]


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (100, get_even_number()),
        (0, []),
    ],
)
def test_filter(value: int, expected_value: List[any]):
    # Testing Filter object for filtering integers.
    actual_value = Filter(
        [lambda a: a % 2 == 0, lambda a: a > 0, lambda a: isinstance(a, int)]
    ).apply(range(value))

    assert actual_value == expected_value


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (
            {"name": "Bill", "type": "person"},
            [
                {
                    "name": "Bill",
                    "last_name": "Gilbert",
                    "occupation": "was here",
                    "type": "person",
                }
            ],
        ),
        ({"name": "polly", "type": "person"}, []),
    ],
)
def test_make_filter(value: Dict[str, any], expected_value: List[Dict[str, any]]):
    # Testing late binding in make_filter
    actual_result = make_filter(**value).apply(sample_data)

    assert actual_result == expected_value
