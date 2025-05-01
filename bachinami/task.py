from __future__ import annotations

import os
import uuid
import asyncio

from typing import Dict, Tuple, Generic, Callable, Sequence

from bachinami import T


class BatchBackgroundTask:
    _result_cache: Dict[str, Sequence[T]] = {}
    _add_condition = asyncio.Condition()
    _return_condition = asyncio.Condition()

    def __init__(
        self,
        func: Callable[[T], Sequence[T]],
        batch_size: int,
        queue_size: int = 128
    ) -> None:
        self._queue = asyncio.LifoQueue(queue_size)

        self._batch_size = batch_size
        self._func = func

        self._futures = []

    def start(self) -> BatchBackgroundTask:
        for _ in range(min(32, os.cpu_count() + 4)):
            self._futures.append(self._loop())

        asyncio.gather(*self._futures)
        return self

    def stop(self) -> BatchBackgroundTask:
        return self

    async def __call__(self, data: Generic[T]) -> Generic[T]:
        if self._batch_size == 1:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._func, [data])[0]

        task_id = await self._add_to_queue(data)
        return await self._get_result(task_id)

    async def _get(self) -> Tuple[Sequence[str], Sequence[T]]:
        async with self._add_condition:
            while self._queue.qsize() <= 0:
                await self._add_condition.wait()

        task_ids = []
        datas = []

        for _ in range(min(self._queue.qsize(), self._batch_size)):
            task_id, data = await self._queue.get()
            task_ids.append(task_id)
            datas.append(data)

        return task_ids, datas

    async def _add_results(self, task_ids: Sequence[str], data: Sequence[T]) -> None:
        async with self._return_condition:
            for task_id, data_item in zip(task_ids, data):
                self._result_cache[task_id] = data_item
                self._return_condition.notify_all()

    async def _loop(self) -> None:
        loop = asyncio.get_event_loop()

        while True:
            task_ids, data = await self._get()

            if len(data):
                result = await loop.run_in_executor(None, self._func, data)
                await self._add_results(task_ids, result)

    async def _add_to_queue(self, data: Generic[T]) -> str:
        task_id = uuid.uuid4().hex

        async with self._return_condition:
            while self._queue.full():
                await self._return_condition.wait()

        async with self._add_condition:
            await self._queue.put((task_id, data))
            self._add_condition.notify_all()

        return task_id

    async def _get_result(self, task_id: str) -> Generic[T]:
        async with self._return_condition:
            while task_id not in self._result_cache:
                await self._return_condition.wait()

        return self._result_cache.pop(task_id)
