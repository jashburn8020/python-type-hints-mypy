"""Alternative constructors."""

from typing import Generic, Tuple, Type, TypeVar

T = TypeVar("T")


class Base(Generic[T]):
    Q = TypeVar("Q", bound="Base[T]")

    def __init__(self, item: T) -> None:
        self.item = item

    @classmethod
    def make_pair(cls: Type[Q], item: T) -> Tuple[Q, Q]:
        return cls(item), cls(item)


class Sub(Base[T]):
    ...


pair = Sub.make_pair("yes")  # Type is "Tuple[Sub[str], Sub[str]]"
reveal_type(pair)
bad = Sub[int].make_pair("no")  # Error
