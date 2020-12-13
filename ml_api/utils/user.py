import uuid
from secrets import token_urlsafe


def generate_api_key() -> str:
    return token_urlsafe(32)


def generate_uuid4() -> str:
    return str(uuid.uuid4())
