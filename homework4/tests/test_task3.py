import pytest
from task_3_get_print_output import my_precious_logger


@pytest.mark.parametrize(
    "value",
    [
        " ",
        "1234",
        "err:123",
    ],
)
def test_stdout(capsys, value: str):
    # Positive test of writing to stdout.
    my_precious_logger(value)
    actual_result = capsys.readouterr().out

    assert actual_result == value


@pytest.mark.parametrize(
    "value",
    [
        "error",
        "error: got an exception",
    ],
)
def test_stderr(capsys, value: str):
    # Positive test of writing to stderr.
    my_precious_logger(value)
    actual_result = capsys.readouterr().err
    assert actual_result == value
