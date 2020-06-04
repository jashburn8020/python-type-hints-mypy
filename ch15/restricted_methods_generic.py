"""Restricted methods in generic classes."""

from typing import Callable, Generic, List, Sequence, TypeVar, overload

T = TypeVar("T")


class Tag(Generic[T]):
    item: T

    def uppercase_item(self: Tag[str]) -> str:
        return self.item.upper()

    @overload
    def export(self: Tag[str]) -> str:
        ...

    @overload
    def export(self, converter: Callable[[T], str]) -> str:
        ...

    def export(self, converter=None):
        if isinstance(self.item, str):
            return self.item
        return converter(self.item)


def label(ti: Tag[int], ts: Tag[str]) -> None:
    ti.uppercase_item()  # Error
    ts.uppercase_item()  # This is OK


S = TypeVar("S")


class Storage(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content = content

    def first_chunk(self: Storage[Sequence[S]]) -> S:
        return self.content[0]


page: Storage[List[str]]
page.first_chunk()  # OK, type is "str"
Storage(0).first_chunk()  # Error
