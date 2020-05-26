"""Generators."""

from typing import Iterator, Generator


def squares(num: int) -> Iterator[int]:
    """Basic generator that only yields values."""
    for i in range(num):
        yield i * i


def echo_round() -> Generator[int, float, str]:
    """Generator to accept values via the `send()` method or return a value."""
    sent = yield 0
    while sent >= 0:
        sent = yield round(sent)
    return "Done"
