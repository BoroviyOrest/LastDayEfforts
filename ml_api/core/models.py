from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from db.postgres import PoolManager


class AbstractModel(ABC):
    def __init__(self, postgres: PoolManager):
        self._postgres = postgres

    @abstractmethod
    async def create(self, *args, **kwargs) -> Type[BaseModel]:
        pass

    async def get_many(self) -> list:
        pass

    async def update(self, *args, **kwargs) -> Type[BaseModel]:
        pass
