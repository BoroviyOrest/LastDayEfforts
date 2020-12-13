from pydantic import EmailStr

from core.exceptions import EntityDoesNotExist
from models.user import UserModel


async def check_email_is_taken(model: UserModel, email: EmailStr) -> bool:
    try:
        await model.get_by_email(email)
    except EntityDoesNotExist:
        return False

    return True
