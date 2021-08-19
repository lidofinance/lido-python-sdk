from concurrent.futures import ThreadPoolExecutor
from asyncio import gather, get_event_loop
from typing import Callable, TypeVar, List, Dict, Any
from itertools import chain
from math import ceil


class Chunk:
    def __init__(self, start_index: int, end_index: int):
        self.start_index = start_index
        self.end_index = end_index

    def __iter__(self):
        self._next = self.start_index
        return self

    def __next__(self):
        if self._next <= self.end_index:
            current = self._next
            self._next += 1
            return current
        else:
            raise StopIteration


def get_chunks(start_index: int, end_index: int, chunk_size: int) -> List[Chunk]:
    assert start_index >= 0
    assert start_index <= end_index
    assert chunk_size > 0

    elements_amount = end_index - start_index + 1
    groups_amount = ceil(elements_amount / chunk_size)

    return [
        Chunk(
            start_index + group_index * chunk_size,
            min(
                start_index + group_index * chunk_size + chunk_size - 1,
                end_index
            )
        )
        for group_index in range(groups_amount)
    ]


A = TypeVar('A')
T = TypeVar('T')


def chunks_multithread_execute(
    max_workers: int,
    chunks: List[Chunk],
    get_processor: Callable[[Chunk], Callable[[], Dict[int, T]]],
) -> List[T]:
    loop = get_event_loop()

    async def loop_execute():
        with ThreadPoolExecutor(max_workers) as executor:
            result = await gather(*[
                loop.run_in_executor(executor, get_processor(chunk))
                for chunk in chunks
            ])

            return list(chain(*result))

    return loop.run_until_complete(loop_execute())
