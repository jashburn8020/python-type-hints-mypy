"""Explicit types for variables."""

from typing import Union

# Mypy checks that the type of the initializer is compatible with the declared type
invalid_initializer: Union[int, str] = 1.1

# Special comment to declare the type of a variable
special_comment_type = 1  # type: Union[int, str]

# Declare variable type without initialization
x: str
