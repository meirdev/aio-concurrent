import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Callable

from .functions import BaseFunction

OnError = Callable[[Exception], None]

OnProgress = Callable[[int, int], None]


def _on_error(error: Exception) -> None:
    pass


def _on_progress(total: int, done: int) -> None:
    pass


class Concurrent:
    def __init__(
        self,
        function: BaseFunction,
        max_workers: int | None = None,
        on_error: OnError | None = None,
        on_progress: OnProgress | None = None,
    ) -> None:
        self._function = function
        self._items = list(function.get_items())

        self._max_workers = max_workers

        self._on_error = on_error or _on_error
        self._on_progress = on_progress or _on_progress

        self._loop = asyncio.get_event_loop()

        self._tasks: set[asyncio.Future] = set()
        self._tasks_done = 0

    def _done_callback(self, future: asyncio.Future) -> None:
        self._tasks_done += 1

        try:
            future.result()
        except Exception as error:
            self._on_error(error)
        finally:
            self._on_progress(len(self._items), self._tasks_done)

        self._tasks.discard(future)

    async def _run_in_executor(self, executor: ThreadPoolExecutor, file: str):
        return await self._loop.run_in_executor(executor, partial(self._function, file))

    async def run(self) -> None:
        with ThreadPoolExecutor(self._max_workers) as executor:
            for item in self._items:
                task = asyncio.create_task(self._run_in_executor(executor, item))
                task.add_done_callback(self._done_callback)

                self._tasks.add(task)

            await asyncio.wait(self._tasks)


async def concurrent(
    function: BaseFunction,
    max_workers: int | None = None,
    on_error: OnError | None = None,
    on_progress: OnProgress | None = None,
) -> None:
    await Concurrent(function, max_workers, on_error, on_progress).run()
