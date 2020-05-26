"""Instance and class attributes."""

from typing import Any, List


class SingleAttribute:
    """Class with a single `present` attribute."""

    def __init__(self, present: int) -> None:
        self.present = present  # inferred attribute of type 'int'


single = SingleAttribute(1)
single.present = 2  # OK
single.absent = 3  # Error


class DeclaredAttribute:
    """Class with declared attribute."""

    attr: List[int]  # Declare attribute 'x' of type List[int]


declared = DeclaredAttribute()
declared.attr = [1]  # OK


class InstanceVarDefinedInMethod:
    """Explicit types to instance variables defined in a method."""

    def __init__(self) -> None:
        self.x: List[int] = []

    def some_func(self) -> None:
        self.y: Any = 0


class InitNoneReturn:
    """`__init__` `None` return type declared."""

    def __init__(self) -> None:
        self.var = 42
