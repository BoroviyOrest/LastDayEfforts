from typing import Optional

from pydantic import BaseModel


class Image(BaseModel):
    id: int
    style_id: int
    raw_image_name: str
    transformed_image_name: Optional[str]
