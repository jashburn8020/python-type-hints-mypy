"""Mixin classes."""

from typing import Protocol


class Lockable(Protocol):
    @property
    def lock(self) -> Lock:
        ...


class AtomicCloseMixin:
    def atomic_close(self: Lockable) -> int:
        with self.lock:
            # perform actions
            ...


class AtomicOpenMixin:
    def atomic_open(self: Lockable) -> int:
        with self.lock:
            # perform actions
            ...


class File(AtomicCloseMixin, AtomicOpenMixin):
    def __init__(self) -> None:
        self.lock = Lock()


class Bad(AtomicCloseMixin):
    pass


f = File()
b: Bad
f.atomic_close()  # OK
b.atomic_close()  # Error: Invalid self type for "atomic_close"
