import asyncio
from time import sleep

import asyncpg

from core import config
from core.celery import celery_app
from models.image import ImageModel


async def update_image(image_id: int, filename: str):
    conn = await asyncpg.connect(
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD,
        database=config.POSTGRES_DB,
        host=config.POSTGRES_HOST)
    await ImageModel.add_transformed_image(conn, image_id, filename)
    await conn.close()


@celery_app.task()
def transform_image_style(image_id: int, raw_file_name: str, style_id: int) -> str:
    sleep(30)
    asyncio.run(update_image(image_id, raw_file_name))
    return f"test task return {raw_file_name}"
