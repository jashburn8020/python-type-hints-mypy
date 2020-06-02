"""Covariance and contravariance."""

import os
from typing import Generic, List, TypeVar


class Shape:
    pass


class Circle(Shape):
    def rotate(self) -> None:
        ...


def add_one(things: List[Shape]) -> None:
    things.append(Shape())


my_things: List[Circle] = []
add_one(my_things)  # This may appear safe, but...
my_things[0].rotate()  # ...this will fail


T = TypeVar("T")
T_co = TypeVar("T_co", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


class LinkedList(Generic[T]):  # invariant by default
    ...

    def append(self, element: T) -> None:
        ...


class Box(Generic[T_co]):  #  this type is declared covariant
    def __init__(self, content: T_co) -> None:
        self._content = content

    def get_content(self) -> T_co:
        return self._content


class Sink(Generic[T_contra]):  # this type is declared contravariant
    def send_to_nowhere(self, data: T_contra) -> None:
        with open(os.devnull, "w") as devnull:
            print(data, file=devnull)
