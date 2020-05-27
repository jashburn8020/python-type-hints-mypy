"""Casts and type assertions."""

from typing import Any, List, cast

o: object = [1]
x = cast(List[int], o)  # OK
y = cast(List[str], o)  # OK (cast performs no actual runtime check)


def foo(o: object) -> None:
    print(o + 5)  # Error: can't add 'object' and 'int'
    assert isinstance(o, int)
    print(o + 5)  # OK: type of 'o' is 'int' here


x_str = 1
x_str.whatever()  # Type check error
y_any = cast(Any, x_str)
y_any.whatever()  # Type check OK (runtime error)
