from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4
from starlette.status import HTTP_404_NOT_FOUND

from core.dependencies import init_model
from core.exceptions import EntityDoesNotExist
from models.user import UserModel
from schema.user import UserInDetails, UserInAdminUpdate

router = APIRouter()


@router.get("/", response_model=List[UserInDetails], name="admin:get_all")
async def get_all_users(model: UserModel = Depends(init_model(UserModel))) -> List[UserInDetails]:
    users = await model.get_many()
    return [UserInDetails(**user) for user in users]


@router.get("/{uuid}", response_model=UserInDetails, name="admin:get_single")
async def get_user(
        uuid: UUID4,
        model: UserModel = Depends(init_model(UserModel))
) -> UserInDetails:
    try:
        user = await model.get_by_uuid(uuid)
        return UserInDetails(**user.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User with this uuid does not exist."
        )


@router.patch("/{uuid}", response_model=UserInDetails, name="admin:patch_update")
async def patch_user(
        uuid: UUID4,
        user_data: UserInAdminUpdate,
        model: UserModel = Depends(init_model(UserModel))
) -> UserInDetails:
    try:
        user = await model.update(uuid, **user_data.dict())
        return UserInDetails(**user.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User with this uuid does not exist."
        )
