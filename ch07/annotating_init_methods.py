"""Annotating `__init__` methods"""


class InitNoNoneReturn:
    """`__init__` return type not declared, but argument is annotated."""

    def __init__(self, arg: int):
        self.var = arg
