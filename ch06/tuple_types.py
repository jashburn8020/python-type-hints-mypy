"""`Tuple` types."""

from typing import Tuple


def tuple_type(some_tuple: Tuple[int, str]) -> None:
    """Fixed-length tuple."""
    some_tuple = 1, "foo"  # OK
    some_tuple = "foo", 1  # Type check error


def var_length_tuple(some_tuple: Tuple[int, ...]) -> None:
    """Variable length tuple."""
    for elem in some_tuple:
        print(elem, elem ** 2)


var_length_tuple(())  # OK
var_length_tuple((1, 3, 5))  # OK
var_length_tuple([1, 2])  # Error: only a tuple is valid
