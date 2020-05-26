"""Overriding statically typed methods."""


class Base:
    def some_func(self, x: int) -> None:
        pass


class Derived1(Base):
    def some_func(self, x: str) -> None:  # Error: type of 'x' incompatible
        pass


class Derived2(Base):
    def some_func(self, x: int, y: int) -> None:  # Error: too many arguments
        pass


class Derived3(Base):
    def some_func(self, x: int) -> None:  # OK
        pass


class Derived4(Base):
    def some_func(self, x: float) -> None:  # OK: mypy treats int as a subtype of float
        pass


class Derived5(Base):
    def some_func(self, x: int, y: int = 0) -> None:  # OK: accepts more than the base
        pass  #     class method


class StaticBase:
    def inc(self, x: int) -> int:
        return x + 1


class DynamicDerived(StaticBase):
    def inc(self, x):  # Override, dynamically typed
        return "hello"  # Incompatible with 'StaticBase', but no mypy error
