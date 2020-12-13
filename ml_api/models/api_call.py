from datetime import datetime as dt
from datetime import MINYEAR
from typing import List

from asyncpg import exceptions
from pydantic import UUID4
from pydantic.schema import datetime

from core.exceptions import EntityDoesNotExist
from core.models import AbstractModel
from schema.api_call import ApiCallInDB, ApiCallInResponse
from schema.image import Image

CREATE_API_CALL = """
    INSERT INTO "API_CALL" (user_uuid, image_id) VALUES ($1, $2) RETURNING id, created_on;
"""
GET_API_CALL_BY_ID = """
    SELECT id, user_uuid, image_id, created_on FROM "API_CALL" WHERE id = $1;
"""
GET_API_CALLS = """
    SELECT "API_CALL".id, user_uuid, image_id, created_on, style_id, raw_image_name, transformed_image_name
    FROM "API_CALL" 
    INNER JOIN "IMAGE" ON image_id="IMAGE".id
    WHERE 
        user_uuid = COALESCE($1, user_uuid) AND 
        style_id = COALESCE($2, style_id) AND
        created_on BETWEEN $3 AND $4;
"""
GET_API_CALLS_COUNT_BY_USER = """
    SELECT count(id) as count FROM "API_CALL" WHERE user_uuid = $1;
"""


class ApiCallModel(AbstractModel):
    async def create(self, user_uuid: UUID4, image_id: int) -> ApiCallInDB:
        try:
            record = await self._postgres.fetch_row(
                CREATE_API_CALL,
                user_uuid,
                image_id
            )
            return ApiCallInDB(
                id=record.get('id'),
                user_uuid=user_uuid,
                image_id=image_id,
                created_on=record.get('created_on')
            )
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_by_id(self, id: int) -> ApiCallInDB:
        try:
            record = await self._postgres.fetch_row(GET_API_CALL_BY_ID, id)
            if record is None:
                raise EntityDoesNotExist

            return ApiCallInDB(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_many(
            self,
            user_uuid: UUID4 = None,
            style_id: int = None,
            from_datetime: datetime = None,
            to_datetime: datetime = None
    ) -> List[ApiCallInResponse]:
        from_datetime = from_datetime or dt(MINYEAR, 1, 1)
        to_datetime = to_datetime or dt.now()

        try:
            records = await self._postgres.fetch(
                GET_API_CALLS,
                user_uuid,
                style_id,
                from_datetime,
                to_datetime
            )

            api_calls: List[ApiCallInResponse] = []
            for record in records:
                image = Image(
                    id=record.get("image_id"),
                    style_id=record.get("style_id"),
                    raw_image_name=record.get("raw_image_name"),
                    transformed_image_name=record.get("transformed_image_name"),
                )
                call = ApiCallInResponse(
                    id=record.get("id"),
                    user_uuid=record.get("user_uuid"),
                    image=image,
                    created_on=record.get("created_on"),
                )
                api_calls.append(call)

            return api_calls
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_api_calls_count_by_user(self, user_uuid: UUID4) -> int:
        try:
            record = await self._postgres.fetch_row(
                GET_API_CALLS_COUNT_BY_USER,
                user_uuid
            )

            return record.get("count")
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass
