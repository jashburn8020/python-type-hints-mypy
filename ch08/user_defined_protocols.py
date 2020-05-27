"""Simple user-defined protocols."""

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
