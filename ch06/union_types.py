"""`Union` types."""

from typing import Union


def union_type(arg: Union[int, str]) -> None:
    """Union type."""
    print(arg + 1)  # Error: str + int is not valid
    if isinstance(arg, int):
        print(arg + 1)  # OK
    else:
        print(arg + "a")  # OK


union_type(1)  # OK
union_type("x")  # OK
union_type(1.1)  # Error
