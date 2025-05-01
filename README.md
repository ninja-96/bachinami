# BachiNami

Batch pipeline processing

## Installation

Install using `pip`\
From source:

```bash
pip3 install git+https://github.com/ninja-96/bachinami
```

## Getting Started

1) Write your function (`my_function`)

```python
def my_function(data: List[int]) -> List[int]:
    return [i + 1 for i in data]
```

2) Import `BatchBackgroundTask` and create instanse

```python
from bachinami.task import BatchBackgroundTask

batch_task = BatchBackgroundTask(my_function, 4)
```

3) Create `FastAPI` application and use `batch_task` in handler

```python
@app.post('/inc/{value}')
async def post_inc(
    value: int,
    task: BatchBackgroundTask = Depends(get_batch_task)
) -> int:
    return await task(value)
```

### Note

- The function **should not change order of elements**
- `my_function` must accept a `Sequence` and return a `Sequence`

## Versioning

All versions available, see the [tags on this repository](https://github.com/ninja-96/bachinami/tags).

## Authors

- **Oleg Kachalov** - _Initial work_ - [ninja-96](https://github.com/ninja-96)

See also the list of [contributors](https://github.com/ninja-96/bachinami/contributors) who participated in this project.

## License

This project is licensed under the GPL-3.0 license - see the [LICENSE.md](./LICENSE) file for details.
