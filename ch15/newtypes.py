"""`NewType`s."""

from typing import NewType

UserId = NewType("UserId", int)


def name_by_id(user_id: UserId) -> str:
    ...


UserId("user")  # Fails type check

name_by_id(42)  # Fails type check
name_by_id(UserId(42))  # OK

num = UserId(5) + 1  # type: int


class PacketId:
    def __init__(self, major: int, minor: int) -> None:
        self._major = major
        self._minor = minor


TcpPacketId = NewType("TcpPacketId", PacketId)

packet = PacketId(100, 100)
tcp_packet = TcpPacketId(packet)  # OK

tcp_packet = TcpPacketId(127, 0)  # Fails in type checker and at runtime
