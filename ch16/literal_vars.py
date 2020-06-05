"""Declaring literal variables."""

from typing import Final, Literal


def expects_literal(x: Literal[19]) -> None:
    pass


c: Final = 19

reveal_type(c)  # Revealed type is 'Literal[19]?'
expects_literal(c)  # ...and this type checks!


a: Final = 19

# Mypy will infer List[int] here.
list_of_ints = []
list_of_ints.append(a)
reveal_type(list_of_ints)  # Revealed type is 'List[int]'

b: Literal[19] = 19

# mypy # will infer List[Literal[19]].
list_of_lits = []
list_of_lits.append(b)
reveal_type(list_of_lits)  # Revealed type is 'List[Literal[19]]'
