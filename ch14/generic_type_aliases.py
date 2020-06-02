"""Generic type aliases."""

from typing import Callable, Iterable, Tuple, TypeVar, Union

S = TypeVar("S")

TInt = Tuple[int, S]
UInt = Union[S, int]
CBack = Callable[..., S]


def response(query: str) -> UInt[str]:  # Same as Union[str, int]
    ...


def activate(cb: CBack[S]) -> S:  # Same as Callable[..., S]
    ...


table_entry: TInt  # Same as Tuple[int, Any]

T = TypeVar("T", int, float, complex)

Vec = Iterable[Tuple[T, T]]


def inproduct(v: Vec[T]) -> T:
    return sum(x * y for x, y in v)


def dilate(v: Vec[T], scale: T) -> Vec[T]:
    return ((x * scale, y * scale) for x, y in v)


v1: Vec[int] = []  # Same as Iterable[Tuple[int, int]]
v2: Vec = []  # Same as Iterable[Tuple[Any, Any]]
v3: Vec[int, int] = []  # Error: Invalid alias, too many type arguments!
