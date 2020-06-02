"""Generic functions."""

from typing import TypeVar, Sequence

T = TypeVar("T")  # Declare type variable


def first(seq: Sequence[T]) -> T:  # Generic function
    return seq[0]


def last(seq: Sequence[T]) -> T:
    """Type variable `T` is reused."""
    return seq[-1]


s = first("foo")  # s has type str.
assert s == "f"
n = first([1, 2, 3])  # n has type int.
assert n == 1
c = last((1 + 2j, 3 + 4j))  # c has type complex.
assert c == 3 + 4j
