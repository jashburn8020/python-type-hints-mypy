"""Class types."""


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
