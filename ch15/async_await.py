"""Typing `async`/`await`."""

import asyncio
from typing import Any, Awaitable, Generator, AsyncIterator


async def format_string(tag: str, count: int) -> str:
    return "T-minus {} ({})".format(count, tag)


async def countdown_1(tag: str, count: int) -> str:
    while count > 0:
        my_str = await format_string(tag, count)  # has type 'str'
        print(my_str)
        await asyncio.sleep(0.1)
        count -= 1
    return "Blastoff!"


loop = asyncio.get_event_loop()
loop.run_until_complete(countdown_1("Millennium Falcon", 5))
loop.close()

my_coroutine = countdown_1("Millennium Falcon", 5)
reveal_type(my_coroutine)  # has type 'Coroutine[Any, Any, str]'


class MyAwaitable(Awaitable[str]):
    def __init__(self, tag: str, count: int) -> None:
        self.tag = tag
        self.count = count

    def __await__(self) -> Generator[Any, None, str]:
        for i in range(self.count, 0, -1):
            print("T-minus {} ({})".format(i, self.tag))
            yield from asyncio.sleep(0.1)
        return "Blastoff!"


def countdown_3(tag: str, count: int) -> Awaitable[str]:
    return MyAwaitable(tag, count)


loop3 = asyncio.get_event_loop()
loop3.run_until_complete(countdown_3("Heart of Gold", 5))
loop3.close()


class arange(AsyncIterator[int]):
    def __init__(self, start: int, stop: int, step: int) -> None:
        self.start = start
        self.stop = stop
        self.step = step
        self.count = start - step

    def __aiter__(self) -> AsyncIterator[int]:
        return self

    async def __anext__(self) -> int:
        self.count += self.step
        if self.count == self.stop:
            raise StopAsyncIteration
        else:
            return self.count


async def countdown_4(tag: str, n: int) -> str:
    async for i in arange(n, 0, -1):
        print("T-minus {} ({})".format(i, tag))
        await asyncio.sleep(0.1)
    return "Blastoff!"


loop4 = asyncio.get_event_loop()
loop4.run_until_complete(countdown_4("Serenity", 5))
loop4.close()
