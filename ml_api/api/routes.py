from fastapi import APIRouter, Depends

from api import admin, api_call, auth, image, style, user
from core.dependencies import authenticate, admin_permissions, validate_api_key

router = APIRouter()
router.include_router(
    auth.router,
    tags=["authentication"],
    prefix="/users"
)
router.include_router(
    user.router,
    tags=["user"],
    prefix="/user",
    dependencies=[Depends(authenticate)]
)
router.include_router(
    image.router,
    tags=["image-transform"],
    prefix="/image",
    dependencies=[Depends(validate_api_key)]
)
router.include_router(
    admin.router,
    tags=["users-admin"],
    prefix="/admin",
    dependencies=[Depends(authenticate), Depends(admin_permissions)]
)
router.include_router(
    style.router_public,
    tags=["style-public"],
    prefix="/style"
)
router.include_router(
    style.router_private,
    tags=["style-admin"],
    prefix="/style",
    dependencies=[Depends(authenticate), Depends(admin_permissions)]
)
router.include_router(
    api_call.router,
    tags=["api_calls-admin"],
    prefix="/api_calls",
    dependencies=[Depends(authenticate), Depends(admin_permissions)]
)
