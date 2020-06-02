"""Generic protocols."""

from typing import TypeVar
from typing_extensions import Protocol

T = TypeVar("T")


class Box(Protocol[T]):
    content: T


def do_stuff(one: Box[str], other: Box[bytes]) -> None:
    ...


class StringWrapper:
    def __init__(self, content: str) -> None:
        self.content = content


class BytesWrapper:
    def __init__(self, content: bytes) -> None:
        self.content = content


do_stuff(StringWrapper("one"), BytesWrapper(b"other"))  # OK

x: Box[float] = ...
y: Box[int] = ...
x = y  # Error -- Box is invariant


class ReadOnlyBoxInv(Protocol[T]):  # Error: covariant type variable expected
    def content(self) -> T:
        ...


T_co = TypeVar("T_co", covariant=True)


class ReadOnlyBoxCov(Protocol[T_co]):  # OK
    def content(self) -> T_co:
        ...


class CovFloatWrapper:
    def content(self) -> float:
        ...


class CovIntWrapper:
    def content(self) -> int:
        ...


ax: ReadOnlyBoxCov[float] = CovFloatWrapper()
ay: ReadOnlyBoxCov[int] = CovIntWrapper()
ax = ay  # OK -- ReadOnlyBoxCov is covariant

az: ReadOnlyBoxCov[float] = CovIntWrapper()  # OK
aerr: ReadOnlyBoxCov[int] = CovFloatWrapper()  # Error


class Linked(Protocol[T]):
    """Generic protocols can be recursive."""

    val: T

    def next(self) -> "Linked[T]":
        ...


class L:
    val: int

    ...  # details omitted

    def next(self) -> "L":
        ...  # details omitted


def last(seq: Linked[T]) -> T:
    ...  # implementation omitted


result = last(L())  # Inferred type of 'result' is 'int'
