"""Function overloading."""

from typing import Optional, Sequence, TypeVar, Union, overload


class ClickEvent:
    def __init__(self, x1: int, y1: int) -> None:
        ...


class DragEvent:
    def __init__(self, x1: int, y1: int, x2: int, y2: int) -> None:
        ...


# Overload *variants* for 'mouse_event'. These variants give extra information to the
# type checker. They are ignored at runtime.


@overload
def mouse_event(x1: int, y1: int) -> ClickEvent:
    ...


@overload
def mouse_event(x1: int, y1: int, x2: int, y2: int) -> DragEvent:
    ...


# The actual *implementation* of 'mouse_event'. The implementation contains the actual
# runtime logic.


def mouse_event(
    x1: int, y1: int, x2: Optional[int] = None, y2: Optional[int] = None
) -> Union[ClickEvent, DragEvent]:
    if x2 is None and y2 is None:
        return ClickEvent(x1, y1)
    elif x2 is not None and y2 is not None:
        return DragEvent(x1, y1, x2, y2)
    else:
        raise TypeError("Bad arguments")


click_event = mouse_event(1, 2)  # OK
click_event = mouse_event(1, 2, 3, 4)  # Error

drag_event = mouse_event(1, 2, 3, 4)  # OK
drag_event = mouse_event(1, 2)  # Error
drag_event = mouse_event(1, 2, 3)  # Error


T = TypeVar("T")


class MyList(Sequence[T]):
    def __init__(self, content: Sequence[T]) -> None:
        self.content = content

    @overload
    def __getitem__(self, index: int) -> T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[T, Sequence[T]]:
        if isinstance(index, int):
            # Return a T here
            return self.content[index]
        elif isinstance(index, slice):
            # Return a sequence of Ts here
            return self.content[index]
        else:
            raise TypeError("Invalid arguments")

    def __len__(self) -> int:
        return len(self.content)


my_list = MyList([1, 2, 3])
my_elem = my_list[1]  # OK
my_elem = my_list[:]  # Error

my_seq = my_list[:]  # OK
my_seq = my_list[1]  # Error
