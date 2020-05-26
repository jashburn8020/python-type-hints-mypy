"""Abstract base classes and multiple inheritance."""

from abc import ABCMeta, abstractmethod


class Animal(metaclass=ABCMeta):
    @abstractmethod
    def eat(self, food: str) -> None:
        pass

    @property
    @abstractmethod
    def can_walk(self) -> bool:
        pass


class Cat(Animal):
    def eat(self, food: str) -> None:
        pass  # Body omitted

    @property
    def can_walk(self) -> bool:
        return True


x = Animal()  # Error: 'Animal' is abstract due to 'eat' and 'can_walk'
y = Cat()  # OK


class Base(metaclass=ABCMeta):
    @abstractmethod
    def base_method(self, x: int) -> None:
        pass


class Derived(Base):  # No error -- Derived is implicitly abstract
    def derived_method(self) -> None:
        pass


d = Derived()  # Error: 'Derived' is abstract
