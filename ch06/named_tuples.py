"""Named tuples."""

from typing import NamedTuple
from collections import namedtuple

# namedtuple - all the items are assumed to have Any types
Point = namedtuple("Point", ["x", "y"])
point = Point(x=1, y="two")

# Use NamedTuple to also define item types
TypedPoint = NamedTuple("TypedPoint", [("x", int), ("y", int)])
# Argument has incompatible type "str"; expected "int"
typed_point = TypedPoint(x=1, y="two")


class ClassBasedPoint(NamedTuple):
    """Class-based syntax for named tuples with types."""

    x: int
    y: int


# Argument has incompatible type "str"; expected "int"
class_based_point = ClassBasedPoint(x=1, y="two")
