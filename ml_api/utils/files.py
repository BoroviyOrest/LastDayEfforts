import os
import uuid
from typing import Optional

from fastapi import UploadFile

from core import config
from core.exceptions import FileWriteError, ValidationError


async def validate_file(file: UploadFile) -> None:
    if file.content_type not in config.ALLOWED_MIME_TYPES:
        mime_types = ", ".join(config.ALLOWED_MIME_TYPES)
        raise ValidationError(
            f"Content type should be: {mime_types}"
        )


async def generate_name() -> str:
    return str(uuid.uuid4())


async def save_file(file: UploadFile) -> Optional[str]:
    extension = file.filename.split(".")[-1]
    name = await generate_name()
    filename = f"{config.RAW_IMAGES_DIR}/{name}.{extension}"

    try:
        with open(filename, "wb") as f:
            bytes_content = await file.read()
            f.write(bytes_content)
        return filename
    except (PermissionError, FileExistsError, FileNotFoundError) as err:
        raise FileWriteError(str(err))


async def delete_file(filename: str) -> None:
    try:
        os.remove(filename)
    except (PermissionError, FileNotFoundError) as err:
        raise FileWriteError(str(err))

