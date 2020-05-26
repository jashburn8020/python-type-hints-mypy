"""Function signatures and dynamic vs static typing"""


def greeting_dynamic(name):
    """Dynamically typed function."""
    return "Hello " + name


greeting_dynamic("stranger")


def greeting_typed(name: str) -> str:
    """Statically typed function."""
    return "Hello " + name


greeting_typed(3)
