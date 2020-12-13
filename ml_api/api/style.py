from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from core.dependencies import init_model
from core.exceptions import EntityDoesNotExist
from models.style import StyleMode
from schema.style import StyleInDB, StyleInCreate

router_public = APIRouter()
router_private = APIRouter()


@router_private.post("/", response_model=StyleInDB, name="style:create_style")
async def create_style(
        style_data: StyleInCreate,
        model: StyleMode = Depends(init_model(StyleMode))
) -> StyleInDB:
    style = await model.create(style_data.description)
    if style is not None:
        return style
    raise HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail="Style was not created."
    )


@router_public.get("/", response_model=List[StyleInDB], name="style:get_all")
async def get_all_styles(model: StyleMode = Depends(init_model(StyleMode))) -> List[StyleInDB]:
    styles = await model.get_many()
    return [StyleInDB(**style) for style in styles]


@router_public.get("/{style_id}", response_model=StyleInDB, name="style:get_single")
async def get_style(
        style_id: int,
        model: StyleMode = Depends(init_model(StyleMode))
) -> StyleInDB:
    try:
        style = await model.get_by_id(style_id)
        return StyleInDB(**style.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Style with this style_id does not exist."
        )


@router_private.put("/{style_id}", response_model=StyleInDB, name="style:update_description")
async def update_description(
        style_id: int,
        style_data: StyleInCreate,
        model: StyleMode = Depends(init_model(StyleMode))
) -> StyleInDB:
    try:
        style = await model.update(style_id, style_data.description)
        return StyleInDB(**style.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Style with this style_id does not exist."
        )
