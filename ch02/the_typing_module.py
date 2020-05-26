"""The `typing` module."""

from typing import Iterable, List, Optional, Union


def complex_static_type(names: List[str]) -> None:
    """Complex static type - `List`."""
    for name in names:
        print("Hello " + name)


complex_static_type(["Alice", "Bob", "Charlie"])
complex_static_type([10, 20])
complex_static_type(("Alice", "Bob", "Charlie"))


def complex_static_type_iterable(names: Iterable[str]) -> None:
    """Complex static type - `Iterable`."""
    for name in names:
        print("Hello " + name)


complex_static_type_iterable(["Alice", "Bob", "Charlie"])
complex_static_type_iterable(("Alice", "Bob", "Charlie"))


def union_type(user_id: Union[int, str]) -> str:
    """`Union` type to accept both `int` and `str`."""
    if isinstance(user_id, int):
        return "user-{}".format(100000 + user_id)
    return user_id


def optional_type(name: Optional[str] = None) -> str:
    """`Optional` type to also accept a `None`."""
    # Optional[str] means the same thing as Union[str, None]
    if name is None:
        name = "stranger"
    return "Hello, " + name
