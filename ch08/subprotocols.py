"""Defining subprotocols and subclassing protocols."""

from typing import Iterable
from typing_extensions import Protocol


class SupportsClose(Protocol):
    def close(self) -> None:
        pass  # Empty method body (explicit '...')


class Resource:  # No SupportsClose base class!
    # ... some methods ...

    def close(self) -> None:
        self.resource.release()


def close_all(items: Iterable[SupportsClose]) -> None:
    for item in items:
        item.close()


close_all([Resource(), open("some/file")])  # Okay!


class SupportsRead(Protocol):
    def read(self, amount: int) -> bytes:
        ...


class TaggedReadableResource(SupportsClose, SupportsRead, Protocol):
    label: str


class AdvancedResource(Resource):
    def __init__(self, label: str) -> None:
        self.label = label

    def read(self, amount: int) -> bytes:
        # some implementation
        ...


resource: TaggedReadableResource
resource = AdvancedResource("handle with care")  # OK


class NotAProtocol(SupportsClose):  # This is NOT a protocol
    new_attr: int


class Concrete:
    new_attr: int = 0

    def close(self) -> None:
        ...


# Error: nominal subtyping used by default
x: NotAProtocol = Concrete()  # Error!
