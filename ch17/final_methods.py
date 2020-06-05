"""Final methods."""

from typing import final, overload


class Base:
    @final
    def common_name(self) -> None:
        ...


class Derived(Base):
    def common_name(self) -> None:  # Error
        ...


class OverloadMethod:
    @overload
    def method(self) -> None:
        ...

    @overload
    def method(self, arg: int) -> int:
        ...

    @final
    def method(self, x=None):
        ...
