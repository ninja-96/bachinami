import pytest

from bachinami.async_task import AsyncBatchBackgroundTask


async def my_function(data):
    return [i + 1 for i in data]


@pytest.mark.parametrize('batch_size', [1, 2, 4, 8])
def test_task_create(batch_size):
    task = AsyncBatchBackgroundTask(my_function, batch_size)
    assert isinstance(task, AsyncBatchBackgroundTask)


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize('data', [1, 2, 4, 8])
async def test_running(data):
    task = AsyncBatchBackgroundTask(my_function, 2)
    task.start()

    result = await task(data)
    assert result == data + 1
