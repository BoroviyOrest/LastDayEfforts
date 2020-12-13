from typing import Optional

from asyncpg import exceptions
from pydantic import UUID4, EmailStr

from core.exceptions import EntityDoesNotExist
from core.models import AbstractModel
from schema.user import UserInDB
from utils.user import generate_api_key

CREATE_USER = """
    INSERT INTO "USER" (uuid, email, name, salt, hashed_password, api_key)
    VALUES ($1, $2, $3, $4, $5, $6);
"""
GET_USER_BY_ID = """
    SELECT uuid, email, name, salt, hashed_password, api_key, calls_per_day_limit, is_active, is_admin FROM "USER"
    WHERE uuid = $1;
"""
GET_USER_BY_EMAIL = """
    SELECT uuid, email, name, salt, hashed_password, api_key, calls_per_day_limit, is_active, is_admin FROM "USER"
    WHERE email = $1;
"""
GET_USER_BY_API_KEY = """
    SELECT uuid, email, name, salt, hashed_password, api_key, calls_per_day_limit, is_active, is_admin FROM "USER"
    WHERE api_key = $1;
"""
GET_USERS = """
    SELECT uuid, email, name, api_key, calls_per_day_limit, is_active, is_admin FROM "USER"
"""
UPDATE_USER = """
    UPDATE "USER"
        SET name = $2, hashed_password = $3, api_key = $4,
         calls_per_day_limit = $5, is_active = $6, is_admin = $7
    WHERE uuid = $1; 
"""


class UserModel(AbstractModel):
    async def create(self, email: EmailStr, name: str, password: str) -> UserInDB:
        user_data = UserInDB(email=email, name=name)
        user_data.generate_password(password)
        user_data.api_key = generate_api_key()
        print(user_data.dict())
        try:
            await self._postgres.execute(
                CREATE_USER,
                user_data.uuid,
                user_data.email,
                user_data.name,
                user_data.salt,
                user_data.hashed_password,
                user_data.api_key
            )
            return user_data
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_by_uuid(self, uuid: UUID4) -> UserInDB:
        try:
            record = await self._postgres.fetch_row(GET_USER_BY_ID, uuid)
            if record is None:
                raise EntityDoesNotExist

            return UserInDB(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_by_email(self, email: EmailStr) -> UserInDB:
        try:
            record = await self._postgres.fetch_row(GET_USER_BY_EMAIL, email)
            if record is None:
                raise EntityDoesNotExist

            return UserInDB(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_by_api_key(self, api_key: str) -> UserInDB:
        try:
            record = await self._postgres.fetch_row(GET_USER_BY_API_KEY, api_key)
            if record is None:
                raise EntityDoesNotExist

            return UserInDB(**record)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass

    async def get_many(self) -> list:
        try:
            return await self._postgres.fetch(GET_USERS)
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            return []

    async def update(
            self,
            uuid: UUID4,
            name: Optional[str] = None,
            api_key: Optional[str] = None,
            password: Optional[str] = None,
            calls_per_day_limit: Optional[int] = None,
            is_active: Optional[bool] = None,
            is_admin: Optional[bool] = None
    ) -> UserInDB:
        user_in_db = await self.get_by_uuid(uuid)

        user_in_db.name = name or user_in_db.name
        user_in_db.api_key = api_key or user_in_db.api_key
        user_in_db.calls_per_day_limit = calls_per_day_limit or user_in_db.calls_per_day_limit
        user_in_db.is_active = is_active if is_active is not None else user_in_db.is_active
        user_in_db.is_admin = is_admin if is_admin is not None else user_in_db.is_admin
        if password is not None:
            user_in_db.generate_password(password)

        try:
            await self._postgres.execute(
                UPDATE_USER,
                user_in_db.uuid,
                user_in_db.name,
                user_in_db.hashed_password,
                user_in_db.api_key,
                user_in_db.calls_per_day_limit,
                user_in_db.is_active,
                user_in_db.is_admin
            )
            return user_in_db
        except (exceptions.PostgresError, ValueError) as err:
            # todo: add logger
            pass
