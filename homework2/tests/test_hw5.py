from collections.abc import Hashable, Iterable
from typing import Optional, Tuple

import pytest
from hw5 import custom_range


@pytest.mark.parametrize(
    ["value", "expected_value"],
    [
        (),
    ],
)
def test_custom_range(
    value: Tuple[Iterable, Hashable, Optional[Hashable], Optional[int]],
    expected_value: Iterable,
):
    # Custom range smoke-test.
    pass
