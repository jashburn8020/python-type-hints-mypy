"""Metaclasses."""

from typing import TypeVar, Type, ClassVar


T = TypeVar("T")


class M(type):
    count: ClassVar[int] = 0

    def make(cls: Type[T]) -> T:
        M.count += 1
        return cls()


class A(metaclass=M):
    pass


a: A = A.make()  # make() is looked up at M; the result is an object of type A
print(A.count)


class B(A):
    pass


b: B = B.make()  # metaclasses are inherited
print(B.count)


class M1(type):
    pass


class M2(type):
    pass


class A1(metaclass=M1):
    pass


class A2(metaclass=M2):
    pass


class B1(A1, metaclass=M2):
    pass  # Error


# At runtime the above definition raises an exception
# TypeError: metaclass conflict: the metaclass of a derived class must be a
# (non-strict) subclass of the metaclasses of all its bases

# Same runtime error as in B1, but mypy does not catch it yet
class B12(A1, A2):
    pass
