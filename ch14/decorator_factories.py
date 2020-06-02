"""Decorator factories."""

from typing import Any, Callable, TypeVar, overload

F = TypeVar("F", bound=Callable[..., Any])


def route(url: str) -> Callable[[F], F]:
    ...


@route(url="/")
def index(request: Any) -> str:
    return "Hello world"


# Bare decorator usage
@overload
def atomic(__func: F) -> F:
    ...


# Decorator with arguments
@overload
def atomic(*, savepoint: bool = True) -> Callable[[F], F]:
    ...


# Implementation
def atomic(__func: Callable[..., Any] = None, *, savepoint: bool = True):
    def decorator(func: Callable[..., Any]):
        ...  # Code goes here

    if __func is not None:
        return decorator(__func)
    else:
        return decorator


# Usage
@atomic
def func1() -> None:
    ...


@atomic(savepoint=False)
def func2() -> None:
    ...
