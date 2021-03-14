"""
Write a function that accepts an URL as input
and count how many letters `i` are present in the HTML by this URL.

Write a test that check that your function works.
Test should use Mock instead of real network interactions.

You can use urlopen* or any other network libraries.
In case of any network error raise ValueError("Unreachable {url}).

Definition of done:
 - function is created
 - function is properly formatted
 - function has positive and negative tests

You will learn:
 - how to test using mocks
 - how to write complex mocks
 - how to raise an exception form mocks
 - do a simple network requests


>>> count_dots_on_i("https://example.com/")
59

* https://docs.python.org/3/library/urllib.request.html#urllib.request.urlopen
"""

from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def count_dots_on_i(url: str) -> int:
    """Return quantity of i's (dots on i's if you wish) in the html."""
    try:
        # with urlopen(url) as response:  # Getting url's html body.
        html = urlopen(url).read().decode("utf-8")
        return html.count("i")
    except (URLError, HTTPError):
        raise ValueError("Unreachable {url}")  # For easier testing.
