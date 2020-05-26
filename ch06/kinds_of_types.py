"""Kinds of types
https://mypy.readthedocs.io/en/stable/kinds_of_types.html"""

from typing import Callable, NamedTuple, Optional, Tuple, Union
from collections import namedtuple


class SuperClass:
    def method_a(self) -> int:  # Type of self inferred (SuperClass)
        return 2


class SubClass(SuperClass):
    def method_a(self) -> int:
        return 3

    def method_b(self) -> int:
        return 4


def print_methods(clazz: SuperClass) -> None:
    print(clazz.method_a())  # 3
    clazz.method_b()  # Error: "SuperClass" has no attribute "method_b"


print_methods(SubClass())  # OK (SubClass is a subclass of SuperClass)


def tuple_type(some_tuple: Tuple[int, str]) -> None:
    """Fixed-length tuple."""
    some_tuple = 1, "foo"  # OK
    some_tuple = "foo", 1  # Type check error


def var_length_tuple(some_tuple: Tuple[int, ...]) -> None:
    """Variable length tuple."""
    for elem in some_tuple:
        print(elem, elem ** 2)


var_length_tuple(())  # OK
var_length_tuple((1, 3, 5))  # OK
var_length_tuple([1, 2])  # Error: only a tuple is valid


def callable_type(num: int, a_callable: Callable[[int], int]) -> int:
    """Callable type."""
    return a_callable(a_callable(num))


def some_callable(num: int) -> int:
    return num + 1


print(callable_type(3, some_callable))  # 5


def arbitrary_call(arbitrary_args_callable: Callable[..., int]) -> int:
    """Callable type with arbitrary arguments."""
    return arbitrary_args_callable("x") + arbitrary_args_callable(y=2)


arbitrary_call(ord)  # No static error, but fails at runtime
arbitrary_call(open)  # Error: does not return an int
arbitrary_call(1)  # Error: 'int' is not callable

# Infer x as int and some_iterator as Iterator[int]
some_iterator = map(lambda x: x + 1, [1, 2, 3])


def union_type(arg: Union[int, str]) -> None:
    """Union type."""
    print(arg + 1)  # Error: str + int is not valid
    if isinstance(arg, int):
        print(arg + 1)  # OK
    else:
        print(arg + "a")  # OK


union_type(1)  # OK
union_type("x")  # OK
union_type(1.1)  # Error


def optional_arg_return(some_str: Optional[str]) -> Optional[int]:
    """Optional type in argument and return value."""
    if not some_str:
        return None  # OK
    # Mypy will infer the type of some_str to be str due to the check against None
    return len(some_str)


class Resource:
    """Mypy does not realize that if initialize() is called, self.path is never None."""

    path: Optional[str] = None

    def initialize(self, path: str) -> None:
        self.path = path

    def read(self) -> str:
        # We require that the object has been initialized.
        # assert self.path is not None
        with open(self.path) as file_obj:  # OK if assert above is uncommented
            return file_obj.read()


resource = Resource()
resource.initialize("/foo/bar")
resource.read()


def same_scope_assignment(i: int) -> None:
    """Type inference when further assignment is done in the same scope."""
    num = None  # Inferred type Optional[int] because of the assignment below
    if i > 0:
        num = i

    print(num)


def no_forward_reference(clazz: SomeClass) -> None:
    """Python does not allow references to a class object before the class is defined.
    """
    pass


def forward_reference(clazz: "SomeClass") -> None:
    """Enter the type as a string literal - forward reference."""
    pass


class SomeClass:
    """Class defined after references."""


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


# # Argument has incompatible type "str"; expected "int"
class_based_point = ClassBasedPoint(x=1, y="two")
