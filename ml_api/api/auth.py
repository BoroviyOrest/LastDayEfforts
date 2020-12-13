from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from core import config
from core.dependencies import init_model
from core.exceptions import EntityDoesNotExist
from models.user import UserModel
from schema.user import UserInResponse, UserInCreate, UserInLogin
from utils.auth import check_email_is_taken
from utils.jwt import create_access_token_for_user

router = APIRouter()


@router.post("/login", response_model=UserInResponse, name="users:login")
async def login(
        user_data: UserInLogin,
        model: UserModel = Depends(init_model(UserModel))
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Email or password is incorrect."
    )

    try:
        user = await model.get_by_email(user_data.email)
    except EntityDoesNotExist as e:
        raise wrong_login_error from e

    if user.check_password(user_data.password) is False:
        raise wrong_login_error

    token = create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        uuid=user.uuid,
        token=token,
        email=user.email,
        name=user.name,
        api_key=user.api_key,
        calls_per_day_limit=user.calls_per_day_limit,
        is_active=user.is_active,
        is_admin=user.is_admin
    )


@router.post("", status_code=HTTP_201_CREATED, response_model=UserInResponse, name="users:register")
async def register(
        user_data: UserInCreate,
        model: UserModel = Depends(init_model(UserModel))
) -> UserInResponse:
    email_is_taken = await check_email_is_taken(model, user_data.email)
    if email_is_taken is True:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Email is taken."
        )

    user = await model.create(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password
    )
    token = create_access_token_for_user(user, str(config.SECRET_KEY))

    return UserInResponse(
        uuid=user.uuid,
        token=token,
        email=user.email,
        name=user.name,
        api_key=user.api_key,
        calls_per_day_limit=user.calls_per_day_limit,
        is_active=user.is_active,
        is_admin=user.is_admin
    )



