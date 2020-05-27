from typing import Iterable
from typing_extensions import Protocol


class SupportsGreeting(Protocol):
    def greeting(self) -> None:
        pass


class Hello:
    def greeting(self) -> None:
        print("hello")


class Hi:
    def greeting(self) -> None:
        print("hi")


def greet_all(items: Iterable[SupportsGreeting]) -> None:
    for item in items:
        item.greeting()


greet_all([Hello(), Hi()])
