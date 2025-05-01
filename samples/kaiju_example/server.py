from typing import List, Sequence

from fastapi import FastAPI, Depends

from kaiju.item import BaseItem
from kaiju.handler import BaseHandler
from kaiju.pipeline import Pipeline
from kaiju.runner import Runner

from bachinami import T
from bachinami.pipeline import BaseBatchPipeline
from bachinami.async_task import AsyncBatchBackgroundTask


class DataItem(BaseItem):
    input_data: List[int] = []
    output_data: List[int] = []


class DataIncHandler(BaseHandler):
    def forward(self, data: DataItem) -> DataItem:
        data.output_data = [i + 1 for i in data.input_data]
        return data


class DataMulHandler(BaseHandler):
    def forward(self, data: DataItem) -> DataItem:
        data.output_data = [i * 2 for i in data.output_data]
        return data


class BatchPipeline(BaseBatchPipeline):
    async def __call__(self, items: Sequence[T]) -> Sequence[T]:
        data_item = DataItem(input_data=items)
        await self._pipeline(data_item)
        return data_item.output_data


app = FastAPI()
pipeline = Pipeline(
    Runner(DataIncHandler()).n_workers(2),
    Runner(DataMulHandler()).n_workers(2)
)
async_batch_task = AsyncBatchBackgroundTask(
    BatchPipeline(pipeline), 8
)


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
