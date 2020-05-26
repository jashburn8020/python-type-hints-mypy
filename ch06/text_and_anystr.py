"""`Text` and `AnyStr`"""

from typing import AnyStr, Text


def unicode_only(unicode_str: Text) -> Text:
    """Accept only unicode strings in a cross-compatible way."""
    return unicode_str + u"\u2713"


def concat(str1: AnyStr, str2: AnyStr) -> AnyStr:
    """Works with any kind of strings, but not mix different types."""
    return str1 + str2


concat("a", "b")  # Okay
concat(b"a", b"b")  # Okay
concat("a", b"b")  # Error: cannot mix bytes and unicode
