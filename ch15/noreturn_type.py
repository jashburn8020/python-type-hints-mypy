"""The `NoReturn` type."""

from typing import NoReturn


def stop() -> NoReturn:
    raise Exception("no way")


def f(x: int) -> int:
    if x == 0:
        return x
    stop()
    return "whatever works"  # No error in an unreachable block
