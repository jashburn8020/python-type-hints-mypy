"""Local type inference."""

from typing import Dict

untyped_global_dict = {}

# If you're using Python 3.6+
annotated_global_dict: Dict[int, float] = {}

# If you want compatibility with older versions of Python
comment_typed_global_dict = {}  # type: Dict[int, float]
