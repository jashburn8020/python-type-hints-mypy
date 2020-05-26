"""Class name forward references."""


def no_forward_reference(clazz: SomeClass) -> None:
    """Python does not allow references to a class object before the class is defined.
    """


def forward_reference(clazz: "SomeClass") -> None:
    """Enter the type as a string literal - forward reference."""


class SomeClass:
    """Class defined after references."""
