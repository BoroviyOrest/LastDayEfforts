from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from core.dependencies import get_current_user, init_model
from core.exceptions import EntityDoesNotExist
from models.user import UserModel
from schema.user import UserInDetails, UserInDB, UserInUpdatePassword
from utils.user import generate_api_key

router = APIRouter()


@router.patch("/password", response_model=UserInDetails, name="user:update_password")
async def update_password(
        password_data: UserInUpdatePassword,
        user: UserInDB = Depends(get_current_user),
        model: UserModel = Depends(init_model(UserModel))
) -> UserInDetails:
    try:
        user = await model.update(user.uuid, password=password_data.password)
        return UserInDetails(**user.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this uuid does not exist."
        )


@router.patch("/update_api_key", response_model=UserInDetails, name="user:update_api_key")
async def update_api_key(
        user: UserInDB = Depends(get_current_user),
        model: UserModel = Depends(init_model(UserModel))
) -> UserInDetails:
    try:
        api_key = generate_api_key()
        user = await model.update(user.uuid, api_key=api_key)
        return UserInDetails(**user.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this uuid does not exist."
        )
