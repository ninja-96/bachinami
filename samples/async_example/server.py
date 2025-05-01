from typing import List
from fastapi import FastAPI, Depends
from bachinami.async_task import AsyncBatchBackgroundTask


async def my_async_function(data: List[int]) -> List[int]:
    return [i + 1 for i in data]


app = FastAPI()
async_batch_task = AsyncBatchBackgroundTask(my_async_function, 4)


def get_async_batch_task() -> AsyncBatchBackgroundTask:
    return async_batch_task


@app.get('/')
async def get_root() -> str:
    return 'OK'


@app.post('/inc/{value}')
async def post_inc(
    value: int,
    task: AsyncBatchBackgroundTask = Depends(get_async_batch_task)
) -> int:
    return await task(value)
