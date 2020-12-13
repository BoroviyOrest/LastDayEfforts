import asyncio
from typing import Callable


def shield(func: Callable) -> Callable:
    """Protect an awaitable object from being cancelled."""

    async def wrapper(*args, **kwargs) -> Callable:
        return await asyncio.shield(func(*args, **kwargs))

    return wrapper


def wait(timeout: int) -> Callable:
    """Wait for the awaitable to complete with a timeout."""

    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs) -> Callable:
            return await asyncio.wait_for(func(*args, **kwargs), timeout)

        return wrapper

    return decorator
