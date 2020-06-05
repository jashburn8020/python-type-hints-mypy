"""Literal types."""

from typing import overload, Union, Literal

# The first two overloads use Literal[...] so we can have precise return types.


@overload
def fetch_data(raw: Literal[True]) -> bytes:
    ...


@overload
def fetch_data(raw: Literal[False]) -> str:
    ...


# The last overload is a fallback in case the caller provides a regular bool.


@overload
def fetch_data(raw: bool) -> Union[bytes, str]:
    ...


def fetch_data(raw: bool) -> Union[bytes, str]:
    # Implementation is omitted
    ...


reveal_type(fetch_data(True))  # Revealed type is 'bytes'
reveal_type(fetch_data(False))  # Revealed type is 'str'

# Variables declared without annotations will continue to have an inferred type of
# 'bool'.

variable = True
reveal_type(fetch_data(variable))  # Revealed type is 'Union[bytes, str]'
