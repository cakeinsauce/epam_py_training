from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

import pytest
from task_2_mock_input import count_dots_on_i


@patch("task_2_mock_input.urlopen", autospec=True)
def test_i_quantity(urlopen):
    # Positive test that count amount of i's.
    read_mock = MagicMock()
    read_mock.read.return_value = b"i I I i 1"

    urlopen.return_value = read_mock

    assert count_dots_on_i(read_mock) == 2


@patch("task_2_mock_input.urlopen", autospec=True)
def test_unreachable_url(urlopen):
    # Negative test unreachable url
    eg_url = "http://example.com/"
    read_mock = MagicMock()
    urlopen.side_effect = HTTPError(
        "http://example.com/", 500, "Internal Error", {}, None
    )
    with pytest.raises(ValueError, match="Unreachable {url}"):
        count_dots_on_i(read_mock)
