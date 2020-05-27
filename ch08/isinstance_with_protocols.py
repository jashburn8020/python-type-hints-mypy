"""Using isinstance() with protocols."""

from typing_extensions import Protocol, runtime_checkable


@runtime_checkable
class Portable(Protocol):
    handles: int


class Mug:
    def __init__(self) -> None:
        self.handles = 1


mug = Mug()
if isinstance(mug, Portable):
    use(mug.handles)  # Works statically and at runtime
