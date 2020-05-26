"""`Callable` types (and lambdas)."""

from typing import Callable


def callable_type(num: int, a_callable: Callable[[int], int]) -> int:
    """Callable type."""
    return a_callable(a_callable(num))


def some_callable(num: int) -> int:
    return num + 1


print(callable_type(3, some_callable))  # 5


def arbitrary_call(arbitrary_args_callable: Callable[..., int]) -> int:
    """Callable type with arbitrary arguments."""
    return arbitrary_args_callable("x") + arbitrary_args_callable(y=2)


arbitrary_call(ord)  # No static error, but fails at runtime
arbitrary_call(open)  # Error: does not return an int
arbitrary_call(1)  # Error: 'int' is not callable

# Infer x as int and some_iterator as Iterator[int]
some_iterator = map(lambda x: x + 1, [1, 2, 3])
