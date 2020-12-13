from typing import Optional

from pydantic import BaseModel, UUID4, EmailStr, Field

from utils.validators import PasswordValidatorMixin
from utils.security import (
    generate_salt,
    get_password_hash,
    verify_password
)
from utils.user import generate_uuid4


class User(BaseModel):
    email: EmailStr
    name: str
    api_key: Optional[str] = None
    calls_per_day_limit: int = 10
    is_active: bool = True
    is_admin: bool = False


class UserInDB(User):
    uuid: UUID4 = Field(default_factory=generate_uuid4)
    salt: str = Field(default_factory=generate_salt)
    hashed_password: str = ""

    def generate_password(self, password: str) -> None:
        self.hashed_password = get_password_hash(self.salt + password)

    def check_password(self, password: str) -> bool:
        return verify_password(self.salt + password, self.hashed_password)


class UserInLogin(BaseModel):
    email: EmailStr
    password: str


class UserInCreate(UserInLogin, PasswordValidatorMixin):
    repeat_password: str
    name: str


class UserInUpdatePassword(BaseModel, PasswordValidatorMixin):
    password: str
    repeat_password: str


class UserInDetails(User):
    uuid: UUID4


class UserInResponse(UserInDetails):
    token: str


class UserInAdminUpdate(BaseModel):
    calls_per_day_limit: Optional[int] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
