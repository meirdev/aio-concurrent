import asyncio
import time
from pathlib import Path

import pytest

from aio_concurrent import concurrent
from aio_concurrent.functions import IOBaseFunction

BASE_DIR = Path(__file__).resolve().parent

ASSERTS = str(BASE_DIR / "assets/**")


class demo(IOBaseFunction):
    def __call__(self, file: str) -> None:
        if not file.endswith(".txt"):
            raise Exception(f"File {file} is not a txt file.")

        time.sleep(3)


@pytest.mark.asyncio
async def test_concurrent(mocker):
    on_error = mocker.stub(name="on_error")
    on_progress = mocker.stub(name="on_progress")

    start = time.time()

    await concurrent(
        demo(ASSERTS),
        max_workers=8,
        on_error=on_error,
        on_progress=on_progress,
    )

    end = time.time()

    assert on_error.call_count == 3
    assert on_progress.call_count == 6

    assert end - start < 3 + 0.5


@pytest.mark.asyncio
async def test_concurrent_gather(mocker):
    spy = mocker.spy(asyncio, "sleep")

    async def foo():
        for _ in range(3):
            await asyncio.sleep(1)

    start = time.time()

    await asyncio.gather(foo(), concurrent(demo(ASSERTS), max_workers=8))

    end = time.time()

    assert end - start < 3 + 0.5

    assert spy.call_count == 3
