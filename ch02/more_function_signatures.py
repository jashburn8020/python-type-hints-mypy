"""More function signatures."""


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
