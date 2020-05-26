"""Starred expressions."""

# Starred expressions
int_1, *ints_a = 1, 2, 3  # OK
int_2, int_3, *ints_b = 1, 2  # Error: Type of ints_b cannot be inferred
