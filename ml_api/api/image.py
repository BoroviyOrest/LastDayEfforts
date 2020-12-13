from typing import Union, List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, BackgroundTasks
from starlette.responses import FileResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from core.celery import celery_app
from core.dependencies import init_model, get_current_user, check_image_retrieve_permission, check_call_limit
from core.exceptions import ValidationError, EntityDoesNotExist
from models.api_call import ApiCallModel
from models.image import ImageModel
from schema.image import Image
from schema.user import UserInDB
from utils.files import validate_file

router = APIRouter()


@router.post(
    "/{api_key}",
    response_model=Image,
    name="image:transform",
    status_code=HTTP_201_CREATED,
    dependencies=[Depends(check_call_limit)]
)
async def transform(
        background_tasks: BackgroundTasks,
        style_id: int = Query(...),
        file: UploadFile = File(...),
        user: UserInDB = Depends(get_current_user),
        api_call_model: ApiCallModel = Depends(init_model(ApiCallModel)),
        image_model: ImageModel = Depends(init_model(ImageModel))
) -> Image:
    try:
        await validate_file(file)
    except ValidationError as err:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=str(err)
        )

    image = await image_model.create(style_id, file)
    if image is None:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="Image was not saved."
        )

    await api_call_model.create(user.uuid, image.id)

    celery_app.send_task("core.tasks.transform_image_style", args=[image.id, image.raw_image_name, image.style_id])

    return image


@router.get(
    "/{api_key}/{image_id}",
    response_model=Image,
    name="image:get_transformed_image",
    dependencies=[Depends(check_image_retrieve_permission)]
)
async def get_image(
        image_id: int,
        model: ImageModel = Depends(init_model(ImageModel))
) -> Union[Image, FileResponse]:
    try:
        image = await model.get_by_id(image_id)
        if image.transformed_image_name is None:
            raise HTTPException(
                status_code=HTTP_200_OK,
                detail="Processing..."
            )
        return FileResponse(image.transformed_image_name)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Image with this image_id does not exist."
        )
