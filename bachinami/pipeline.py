from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    from kaiju.pipeline import Pipeline

from bachinami import T


class BaseBatchPipeline(metaclass=ABCMeta):
    def __init__(self, pipeline: Pipeline) -> None:
        self._pipeline = pipeline

    @abstractmethod
    async def __call__(self, items: Sequence[T]) -> Sequence[T]:
        pass
