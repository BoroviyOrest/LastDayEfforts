from typing import Callable

from fastapi import FastAPI

from db.postgres import PoolManager


def on_startup_handler(app: FastAPI) -> Callable:
    """Create asyncpg pool on the startup."""

    async def start_app() -> None:
        app.state.postgres = await PoolManager.create()

    return start_app


def on_shutdown_handler(app: FastAPI) -> Callable:
    """Close asyncpg pool before shutdown."""

    async def shut_down() -> None:
        await app.state.postgres.close()

    return shut_down
