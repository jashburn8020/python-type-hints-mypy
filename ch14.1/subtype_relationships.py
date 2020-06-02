"""Subtype relationships."""

from typing import List

lucky_number = 3.14  # type: float
lucky_number = 42  # Safe
lucky_number * 2  # This works
lucky_number << 5  # Fails

unlucky_number = 13  # type: int
unlucky_number << 5  # This works
unlucky_number = 2.72  # Unsafe


def append_pi(lst: List[float]) -> None:
    lst += [3.14]


my_list = [1, 3, 5]  # type: List[int]
append_pi(my_list)  # Naively, this should be safe...
my_list[-1] << 5  # ... but this fails
