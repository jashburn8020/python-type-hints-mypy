"""Compatibility of container types."""

from typing import List


def incompatible_lists(object_list: List[object], int_list: List[int]) -> None:
    """Incompatible container types."""
    object_list = int_list
