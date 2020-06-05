"""Final names."""

from typing import Final, List

RATE: Final = 3000


class Base:
    DEFAULT_ID: Final = 0


RATE = 300  # Error
Base.DEFAULT_ID = 1  # Error


class Window:
    BORDER_WIDTH: Final = 2.5
    ...


class ListView(Window):
    BORDER_WIDTH = 3  # Error


class ImmutablePoint:
    x: Final[int]
    y: Final[int]  # Error: final attribute without an initializer

    def __init__(self) -> None:
        self.x = 1


x: List[Final[int]] = []  # Error!


def fun(x: Final[List[int]]) -> None:  # Error!
    ...
