import os
from typing import List, Any

import asyncpg
from asyncpg import Record

from core import config
from core.decorators import wait, shield


class PoolManager:
    """Class that provides postgres executions via pool manager."""

    def __init__(self) -> None:
        """Initialize connections pool manager from env configs."""
        self.pool = None

        self.dsn = config.POSTGRES_DSN
        self.host = config.POSTGRES_HOST
        self.port = config.POSTGRES_PORT

        self.user = config.POSTGRES_USER
        self.password = config.POSTGRES_PASSWORD
        self.database = config.POSTGRES_DB

        self.connection_min_size = config.POSTGRES_CONNECTION_MIN_SIZE
        self.connection_max_size = config.POSTGRES_CONNECTION_MAX_SIZE

    @classmethod
    async def create(cls) -> "PoolManager":
        """Create and initialize pool manager for postgres connections."""
        instance = cls()
        instance.pool = await asyncpg.create_pool(
            dsn=instance.dsn,
            host=instance.host,
            port=instance.port,
            database=instance.database,
            user=instance.user,
            password=instance.password,
            min_size=instance.connection_min_size,
            max_size=instance.connection_max_size,
        )

        return instance

    @wait(timeout=10)
    async def close(self) -> None:
        """
            Close gracefully all connections in the pool with a timeout.
            Errors raised will cause immediate pool termination.
        """
        await self.pool.close()

    @shield
    async def execute(self, query: str, *query_args: Any) -> str:
        """Execute an SQL command (or commands)."""
        async with self.pool.acquire() as con:
            print(query)
            return await con.execute(query, *query_args)

    async def fetch(self, query: str, *query_args: Any) -> List[Record]:
        """Run a query and return the results as a list."""
        async with self.pool.acquire() as con:
            return await con.fetch(query, *query_args)

    @shield
    async def fetch_row(self, query: str, *query_args: Any) -> Record:
        """Run a query and return the first row."""
        async with self.pool.acquire() as con:
            return await con.fetchrow(query, *query_args)
