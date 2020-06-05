"""Final classes."""

from abc import ABCMeta, abstractmethod
from typing import final


@final
class Leaf:
    ...


class MyLeaf(Leaf):  # Error
    ...


@final
class A(metaclass=ABCMeta):  # Error
    @abstractmethod
    def f(self, x: int) -> None:
        pass
