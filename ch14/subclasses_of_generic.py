"""Defining sub-classes of generic classes."""

from typing import Any, Dict, Generic, Iterator, Mapping, TypeVar

KT = TypeVar("KT")
VT = TypeVar("VT")


class MyMap(Mapping[KT, VT]):
    """This is a generic subclass of Mapping."""

    def __getitem__(self, k: KT) -> VT:
        ...  # Implementations omitted

    def __iter__(self) -> Iterator[KT]:
        ...

    def __len__(self) -> int:
        ...


items: MyMap[str, int]  # Okay


class StrDict(Dict[str, str]):
    """This is a non-generic subclass of Dict."""

    def __str__(self) -> str:
        return "StrDict({})".format(super().__str__())


data: StrDict[int, int]  # Error! StrDict is not generic
data2: StrDict  # OK

T = TypeVar("T")


class Receiver(Generic[T]):
    def accept(self, value: T) -> None:
        ...


class AdvancedReceiver(Receiver[T]):
    ...


S = TypeVar("S")
U = TypeVar("U")
V = TypeVar("V")


class One(Generic[V]):
    ...


class Another(Generic[V]):
    ...


class First(One[V], Another[S]):
    ...


class Second(One[V], Another[S], Generic[S, U, V]):
    ...


x: First[int, str]  # Here V is bound to int, S is bound to str
y: Second[int, str, Any]  # Here S is int, U is str, and V is Any
