"""Type inference and type annotations
https://mypy.readthedocs.io/en/stable/type_inference_and_annotations.html"""

from typing import Union, List, Dict, Set

# Mypy checks that the type of the initializer is compatible with the declared type
invalid_initializer: Union[int, str] = 1.1

# Special comment to declare the type of a variable
special_comment_type = 1  # type: Union[int, str]

# Declare variable type without initialization
x: str

# Type annotation for empty collections
empty_list: List[int] = []
empty_dict: Dict[str, int] = {}
empty_set: Set[int] = set()


def incompatible_lists(object_list: List[object], int_list: List[int]) -> None:
    """Incompatible container types."""
    object_list = int_list


def type_context_assignment_target(object_list: List[object]) -> None:
    """Type context is determined by the assignment target."""
    object_list = [1, 2]  # Infer type List[object] for [1, 2], not List[int]


def declared_arg_type_context(int_list: List[int]) -> None:
    """Declared argument types are used for type context."""
    print("Items:", "".join(str(a) for a in int_list))


declared_arg_type_context([])  # OK

# Declaring multiple variables - only with type comment
multiple_vars_int, multiple_vars_bool = 0, False  # type: int, bool

# Starred expressions
int_1, *ints_a = 1, 2, 3  # OK
int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferred
