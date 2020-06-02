"""Defining generic classes."""

from typing import Generic, List, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    def __init__(self, content: Optional[List[T]] = None) -> None:
        if content is None:
            self.items = []
        else:
            self.items = content

    def push(self, item: T) -> None:
        self.items.append(item)

    def pop(self) -> T:
        return self.items.pop()

    def empty(self) -> bool:
        return not self.items


# Construct an empty Stack[int] instance
stack = Stack[int]()
stack.push(2)
stack.pop()
assert stack.empty()
stack.push("x")  # Type error


def process(stack: Stack[int]) -> None:
    ...


process(Stack())  # Argument has inferred type Stack[int]


str_stack = Stack(["a", "b"])  # OK, inferred type is Stack[str]
assert not stack.empty()
str_stack.push(2)  # Type error
