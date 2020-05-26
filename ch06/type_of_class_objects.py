"""The type of class objects."""

from typing import Type, TypeVar


class User:
    # Defines fields like name, email
    pass


class BasicUser(User):
    def upgrade(self) -> None:
        """Upgrade to Pro"""


class ProUser(User):
    def pay(self) -> None:
        """Pay bill"""


def new_user(user_class: type) -> User:
    """The best we can do without Type."""
    user = user_class()
    # (Here we could write the user object to a database)
    return user


buyer = new_user(ProUser)
buyer.pay()  # Rejected, not a method on User


U = TypeVar("U", bound=User)


def typed_new_user(user_class: Type[U]) -> U:
    user = user_class()
    # (Here we could write the user object to a database)
    return user


beginner = typed_new_user(BasicUser)  # Inferred type is BasicUser
beginner.upgrade()  # OK
