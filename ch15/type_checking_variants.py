"""Type checking the variants."""

from typing import Union, overload


class Expression:
    # ...snip...
    ...


class Literal(Expression):
    # ...snip...
    ...


# Warning -- the first overload variant shadows the second!


@overload
def add(left: Expression, right: Expression) -> Expression:
    ...


@overload
def add(left: Literal, right: Literal) -> Literal:
    ...


def add(left: Expression, right: Expression) -> Expression:
    # ...snip...
    ...


@overload
def unsafe_func(x: int) -> int:
    ...


@overload
def unsafe_func(x: object) -> str:
    ...


def unsafe_func(x: object) -> Union[int, str]:
    if isinstance(x, int):
        return 42
    else:
        return "some string"


some_obj: object = 42
x = unsafe_func(some_obj) + " danger danger"  # Type checks, yet crashes at runtime!
reveal_type(x)
