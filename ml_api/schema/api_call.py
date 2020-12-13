from pydantic import BaseModel, UUID4
from pydantic.schema import datetime

from schema.image import Image


class ApiCallInCreate(BaseModel):
    user_uuid: UUID4
    image_id: int


class ApiCallInDB(ApiCallInCreate):
    id: int
    created_on: datetime


class ApiCallInResponse(BaseModel):
    id: int
    user_uuid: UUID4
    image: Image
    created_on: datetime
