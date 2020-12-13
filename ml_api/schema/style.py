from pydantic import BaseModel


class StyleInCreate(BaseModel):
    description: str


class StyleInDB(StyleInCreate):
    id: int
