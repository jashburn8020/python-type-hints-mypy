"""Type variables with value restriction."""

from typing import AnyStr, Union


def concat(x: AnyStr, y: AnyStr) -> AnyStr:
    return x + y


concat("a", "b")  # Okay
concat(b"a", b"b")  # Okay
concat(1, 2)  # Error!
concat("string", b"bytes")  # Error!


def union_concat(x: Union[str, bytes], y: Union[str, bytes]) -> Union[str, bytes]:
    return x + y  # Error: can't concatenate str and bytes


class S(str):
    pass


ss = concat(S("foo"), S("bar"))
assert isinstance(ss, str)
