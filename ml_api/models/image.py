from typing import Optional

from asyncpg import exceptions
from fastapi import UploadFile
from pydantic import UUID4

from core.exceptions import EntityDoesNotExist, FileWriteError
from core.models import AbstractModel
from schema.image import Image
from utils.files import save_file, delete_file

CREATE_IMAGE = """
    INSERT INTO "IMAGE" (style_id, raw_image_name) VALUES ($1, $2) RETURNING id;
"""
GET_IMAGE_BY_ID = """
    SELECT id, style_id, raw_image_name, transformed_image_name FROM "IMAGE" WHERE id = $1;
"""
GET_IMAGE_BY_USER_UUID_AND_STYLE_ID = """
    SELECT id FROM "API_CALL"
    WHERE user_uuid = $1 AND image_id = $2;
"""
ADD_TRANSFORMED_IMAGE = """
    UPDATE "IMAGE" SET transformed_image_name = $2 WHERE id = $1; 
"""


class ImageModel(AbstractModel):
    async def create(self, style_id: int, file: UploadFile) -> Optional[Image]:
        try:
            filename = await save_file(file)
        except FileWriteError as err:
            # todo: add logger
            return

        try:
            record = await self._postgres.fetch_row(
                CREATE_IMAGE,
                style_id,
                filename
            )
            return Image(
                id=record.get('id'),
                style_id=style_id,
                raw_image_name=filename
            )
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            await delete_file(filename)

    async def get_by_id(self, image_id: int) -> Image:
        try:
            record = await self._postgres.fetch_row(GET_IMAGE_BY_ID, image_id)
            if record is None:
                raise EntityDoesNotExist
            print(*record.items())
            return Image(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def check_ownership(self, user_uuid: UUID4, image_id: int) -> Image:
        try:
            record = await self._postgres.fetch_row(
                GET_IMAGE_BY_USER_UUID_AND_STYLE_ID,
                user_uuid,
                image_id
            )
            if record is None:
                raise EntityDoesNotExist

            return Image(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    @staticmethod
    async def add_transformed_image(conn, image_id: int, filename: str):
        try:
            await conn.execute(
                ADD_TRANSFORMED_IMAGE,
                image_id,
                filename
            )
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass
