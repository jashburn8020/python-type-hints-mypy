"""Declaring decorators."""

from typing import Any, Callable, TypeVar, cast

F = TypeVar("F", bound=Callable[..., Any])

# A decorator that preserves the signature.
def my_decorator(func: F) -> F:
    def wrapper(*args, **kwds):
        print("Calling", func)
        return func(*args, **kwds)

    return cast(F, wrapper)


# A decorated function.
@my_decorator
def foo(a: int) -> str:
    return str(a)


a = foo(12)
reveal_type(a)  # str
foo("x")  # Type check error: incompatible type "str"; expected "int"
