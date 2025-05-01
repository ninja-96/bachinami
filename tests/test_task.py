import pytest

from bachinami.task import BatchBackgroundTask


def my_function(data):
    return [i + 1 for i in data]


@pytest.mark.parametrize('batch_size', [1, 2, 4, 8])
def test_task_create(batch_size):
    task = BatchBackgroundTask(my_function, batch_size)
    assert isinstance(task, BatchBackgroundTask)


@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize('data', [1, 2, 4, 8])
async def test_running(data):
    task = BatchBackgroundTask(my_function, 2)
    task.start()

    result = await task(data)
    assert result == data + 1


@pytest.mark.asyncio
@pytest.mark.parametrize('batch_size', [2, 4, 8])
@pytest.mark.parametrize('item_count', [1, 2, 4, 8])
async def test_add_item(batch_size, item_count):
    task = BatchBackgroundTask(my_function, batch_size)

    for i in range(item_count):
        await task._add_to_queue(i)

    assert task._queue.qsize() == item_count


@pytest.mark.asyncio
@pytest.mark.parametrize('batch_size', [2, 4, 8])
async def test_get_data(batch_size):
    task = BatchBackgroundTask(my_function, batch_size)

    for i in range(16):
        await task._add_to_queue(i)

    items = await task._get()
    assert len(items) <= batch_size


@pytest.mark.asyncio
@pytest.mark.parametrize('item_count', [1, 2, 4, 8])
async def test_add_result(item_count):
    task = BatchBackgroundTask(my_function, 16)

    for _ in range(16):
        await task._add_results(
            [f'task_{i}' for i in range(item_count)],
            list(range(item_count))
        )

    assert len(task._result_cache) == item_count


@pytest.mark.asyncio
@pytest.mark.parametrize('item_count', [1, 2, 4, 8])
async def test_get_result(item_count):
    task = BatchBackgroundTask(my_function, 16)

    await task._add_results(
        [f'task_{i}' for i in range(item_count)],
        list(range(item_count))
    )

    for i in range(item_count):
        assert f'task_{i}' in task._result_cache
        item = await task._get_result(f'task_{i}')
        assert item == i
