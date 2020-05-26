"""Context in type inference."""

from typing import List


def type_context_assignment_target(object_list: List[object]) -> None:
    """Type context is determined by the assignment target."""
    object_list = [1, 2]  # Infer type List[object] for [1, 2], not List[int]


def declared_arg_type_context(int_list: List[int]) -> None:
    """Declared argument types are used for type context."""
    print("Items:", "".join(str(a) for a in int_list))


declared_arg_type_context([])  # OK
