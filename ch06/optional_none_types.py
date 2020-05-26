"""`Optional` types and the `None` type."""
from typing import Optional


def optional_arg_return(some_str: Optional[str]) -> Optional[int]:
    """Optional type in argument and return value."""
    if not some_str:
        return None  # OK
    # Mypy will infer the type of some_str to be str due to the check against None
    return len(some_str)


class Resource:
    """Mypy does not realize that if initialize() is called, self.path is never None."""

    path: Optional[str] = None

    def initialize(self, path: str) -> None:
        self.path = path

    def read(self) -> str:
        # We require that the object has been initialized.
        # assert self.path is not None
        with open(self.path) as file_obj:  # OK if assert above is uncommented
            return file_obj.read()


resource = Resource()
resource.initialize("/foo/bar")
resource.read()


def same_scope_assignment(i: int) -> None:
    """Type inference when further assignment is done in the same scope."""
    num = None  # Inferred type Optional[int] because of the assignment below
    if i > 0:
        num = i

    print(num)
