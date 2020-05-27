"""Predefined protocols."""

from typing import Iterator, Iterable, Optional


class IntList:
    def __init__(self, value: int, next: Optional["IntList"]) -> None:
        self.value = value
        self.next = next

    def __iter__(self) -> Iterator[int]:
        current: Optional[IntList] = self
        while current:
            yield current.value
            current = current.next


def print_numbered(items: Iterable[int]) -> None:
    for n, x in enumerate(items):
        print(n + 1, x)


x = IntList(3, IntList(5, None))
print_numbered(x)  # OK
print_numbered([4, 5])  # Also OK
