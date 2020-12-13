from typing import Callable

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import UUID4
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from core import config
from core.exceptions import EntityDoesNotExist
from models.api_call import ApiCallModel
from models.image import ImageModel
from models.user import UserModel
from schema.user import UserInDB
from utils.jwt import get_uuid_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def init_model(model_class) -> Callable:
    def wrapper(request: Request) -> object:
        return model_class(request.app.state.postgres)

    return wrapper


async def authenticate(
        request: Request,
        token: str = Depends(oauth2_scheme),
        model: UserModel = Depends(init_model(UserModel))
):
    try:
        uuid = get_uuid_from_token(token, str(config.SECRET_KEY))
        user = await model.get_by_uuid(UUID4(uuid))
        if user.is_active is False:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You are banned on this service.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user = user
    except (ValueError, EntityDoesNotExist):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def admin_permissions(request: Request) -> None:
    if request.state.user.is_admin is False:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You don't have permission to use this endpoint.",
        )


async def validate_api_key(
        request: Request,
        model: UserModel = Depends(init_model(UserModel))
) -> None:
    api_key = request.path_params.get("api_key")
    try:
        user = await model.get_by_api_key(api_key)
        request.state.user = user
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You don't have permission to use this endpoint.",
        )


async def get_current_user(request: Request) -> UserInDB:
    return request.state.user


async def check_image_retrieve_permission(
        request: Request,
        model: ImageModel = Depends(init_model(ImageModel))
) -> None:
    current_user = request.state.user
    if current_user.is_admin is True:
        return

    image_id = int(request.path_params.get("image_id"))
    try:
        await model.check_ownership(current_user.uuid, image_id)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="You don't have permission to retrieve this image.",
        )


async def check_call_limit(
        user: UserInDB = Depends(get_current_user),
        model: ApiCallModel = Depends(init_model(ApiCallModel))
) -> None:
    count = await model.get_api_calls_count_by_user(user.uuid)
    if count > user.calls_per_day_limit:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=f"You've exceeded limit in {user.calls_per_day_limit} calls'.",
        )
