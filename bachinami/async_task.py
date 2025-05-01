from typing import Generic, Callable, Sequence, Awaitable

from bachinami import T
from bachinami.task import BatchBackgroundTask


class AsyncBatchBackgroundTask(BatchBackgroundTask):
    def __init__(
        self,
        func: Awaitable[Callable[[T], Sequence[T]]],
        batch_size: int,
        queue_size: int = 128,
    ) -> None:
        super().__init__(func, batch_size, queue_size)

    async def __call__(self, data: Generic[T]) -> Generic[T]:
        if self._batch_size == 1:
            return await self._func([data])[0]

        task_id = await self._add_to_queue(data)
        return await self._get_result(task_id)

    async def _loop(self) -> None:
        while True:
            task_ids, task_datas = await self._get()

            if len(task_datas):
                result = await self._func(task_datas)
                await self._add_results(task_ids, result)
