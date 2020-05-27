"""Callback protocols."""

from typing import Callable, Iterable, List, Optional, TypeVar
from typing_extensions import Protocol


class Combiner(Protocol):
    def __call__(self, *vals: bytes, maxlen: Optional[int] = None) -> List[bytes]:
        ...


def batch_proc(data: Iterable[bytes], cb_results: Combiner) -> bytes:
    for item in data:
        ...


def good_cb(*vals: bytes, maxlen: Optional[int] = None) -> List[bytes]:
    ...


def bad_cb(*vals: bytes, maxitems: Optional[int]) -> List[bytes]:
    ...


batch_proc([], good_cb)  # OK
# Error! Argument 2 has incompatible type because of different name and kind in the
# callback
batch_proc([], bad_cb)


T = TypeVar("T")


class Copy(Protocol):
    def __call__(self, __origin: T) -> T:
        ...


copy_a: Callable[[T], T]
copy_b: Copy

copy_a = copy_b  # OK
copy_b = copy_a  # Also OK
