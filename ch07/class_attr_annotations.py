"""Class attribute annotations"""

from typing import ClassVar


class ClassVariable:
    """`ClassVar` annotation."""

    var: ClassVar[int] = 0  # Class variable only


ClassVariable.var += 1  # OK

class_var = ClassVariable()
class_var.var = 1  # Error
print(class_var.var)  # OK -- can be read through an instance
