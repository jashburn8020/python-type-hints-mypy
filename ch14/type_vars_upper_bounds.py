"""Type variables with upper bounds."""

from typing import SupportsAbs, TypeVar

T = TypeVar("T", bound=SupportsAbs[float])


def largest_in_absolute_value(*xs: T) -> T:
    return max(xs, key=abs)  # Okay, because T is a subtype of SupportsAbs[float].


largest_in_absolute_value(-3.5, 2)  # Okay, has type float.
largest_in_absolute_value(5 + 6j, 7)  # Okay, has type complex.
# Error: 'str' is not a subtype of SupportsAbs[float].
largest_in_absolute_value("a", "b")
