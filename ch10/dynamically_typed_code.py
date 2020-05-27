"""Dynamically typed code."""

from typing import Any

s = 1  # Statically typed (type int)
s = "x"  # Type check error

d: Any = 1  # Dynamically typed (type Any)
d = "x"  # OK
