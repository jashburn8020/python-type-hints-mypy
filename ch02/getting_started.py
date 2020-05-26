"""Getting Started
https://mypy.readthedocs.io/en/stable/getting_started.html"""

from typing import List, Iterable, Union, Optional, Dict


def greeting_dynamic(name):
    """Dynamically typed function."""
    return "Hello " + name


greeting_dynamic("stranger")


def greeting_typed(name: str) -> str:
    """Statically typed function."""
    return "Hello " + name


greeting_typed(3)


def no_return() -> None:
    """No return value."""
    print("hello")


some_value = no_return()


def argument_default_value(name: str, excited: bool = False) -> str:
    """Argument with default value."""
    message = "Hello, {}".format(name)
    if excited:
        message += "!!!"
    return message


def args_and_kwargs(*args: int, **kwargs: float) -> None:
    """Annotating `*args` and `**kwargs` arguments."""
    # 'args' has type 'Tuple[int, ...]' (a tuple of ints)
    # 'kwargs' has type 'Dict[str, float]' (a dict of strs to floats)
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print(key, value)


def complex_static_type(names: List[str]) -> None:
    """Complex static type - `List`."""
    for name in names:
        print("Hello " + name)


complex_static_type(["Alice", "Bob", "Charlie"])
complex_static_type([10, 20])
complex_static_type(("Alice", "Bob", "Charlie"))


def complex_static_type_iterable(names: Iterable[str]) -> None:
    """Complex static type - `Iterable`."""
    for name in names:
        print("Hello " + name)


complex_static_type_iterable(["Alice", "Bob", "Charlie"])
complex_static_type_iterable(("Alice", "Bob", "Charlie"))


def union_type(user_id: Union[int, str]) -> str:
    """`Union` type to accept both `int` and `str`."""
    if isinstance(user_id, int):
        return "user-{}".format(100000 + user_id)
    return user_id


def optional_type(name: Optional[str] = None) -> str:
    """`Optional` type to also accept a `None`."""
    # Optional[str] means the same thing as Union[str, None]
    if name is None:
        name = "stranger"
    return "Hello, " + name


untyped_global_dict = {}

# If you're using Python 3.6+
annotated_global_dict: Dict[int, float] = {}

# If you want compatibility with older versions of Python
comment_typed_global_dict = {}  # type: Dict[int, float]
