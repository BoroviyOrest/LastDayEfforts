from asyncpg import exceptions

from core.exceptions import EntityDoesNotExist
from core.models import AbstractModel
from schema.style import StyleInDB

CREATE_STYLE = """
    INSERT INTO "STYLE" (description) VALUES ($1) RETURNING id;
"""
GET_STYLE_BY_ID = """
    SELECT id, description FROM "STYLE" WHERE id = $1;
"""
GET_STYLES = """
    SELECT id, description FROM "STYLE";
"""
UPDATE_STYLE = """
    UPDATE "STYLE" SET description = $2 WHERE id = $1;
"""


class StyleMode(AbstractModel):
    async def create(self, description: str) -> StyleInDB:
        try:
            record = await self._postgres.fetch_row(
                CREATE_STYLE,
                description
            )
            return StyleInDB(id=record.get('id'), description=description)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_by_id(self, id: int) -> StyleInDB:
        try:
            record = await self._postgres.fetch_row(GET_STYLE_BY_ID, id)
            if record is None:
                raise EntityDoesNotExist

            return StyleInDB(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_many(self) -> list:
        try:
            return await self._postgres.fetch(GET_STYLES)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            return []

    async def update(self, id: int, description: str) -> StyleInDB:
        try:
            await self._postgres.fetch_row(
                UPDATE_STYLE,
                id,
                description
            )
            return StyleInDB(id=id, description=description)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

