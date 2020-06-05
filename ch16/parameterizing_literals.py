"""Parameterizing literals."""

from typing import Literal

PrimaryColors = Literal["red", "blue", "yellow"]
SecondaryColors = Literal["purple", "green", "orange"]
AllowedColors = Literal[PrimaryColors, SecondaryColors]


def paint(color: AllowedColors) -> None:
    ...


paint("red")  # Type checks!
paint("turquoise")  # Does not type check
