from typing import List
from fastapi import FastAPI, Depends
from bachinami.task import BatchBackgroundTask


def my_function(data: List[int]) -> List[int]:
    return [i + 1 for i in data]


app = FastAPI()
batch_task = BatchBackgroundTask(my_function, 4)


def get_batch_task() -> BatchBackgroundTask:
    return batch_task


@app.get('/')
async def get_root() -> str:
    return 'OK'


@app.post('/inc/{value}')
async def post_inc(
    value: int,
    task: BatchBackgroundTask = Depends(get_batch_task)
) -> int:
    return await task(value)
