"""Generic methods and generic self."""

from typing import Tuple, Type, TypeVar

# Defines that `Shape` is the upper bound, i.e., an actual type substituted (explicitly
# or implicitly) for the type variable must be a subclass of the boundary type.
T = TypeVar("T", bound="Shape")


class Shape:
    def set_scale(self: T, scale: float) -> T:
        self.scale = scale
        return self


class Circle(Shape):
    def set_radius(self, r: float) -> "Circle":
        self.radius = r
        return self


class Square(Shape):
    def set_width(self, w: float) -> "Square":
        self.width = w
        return self


circle = Circle().set_scale(0.5).set_radius(2.7)  # type: Circle
square = Square().set_scale(0.5).set_width(3.2)  # type: Square

U = TypeVar("U", bound="Friend")


class Friend:
    other = None  # type: Friend

    @classmethod
    def make_pair(cls: Type[U]) -> Tuple[U, U]:
        a, b = cls(), cls()
        a.other = b
        b.other = a
        return a, b


class SuperFriend(Friend):
    pass


a, b = SuperFriend.make_pair()
assert isinstance(a, SuperFriend)
