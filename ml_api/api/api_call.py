from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import UUID4
from pydantic.schema import datetime
from starlette.status import HTTP_404_NOT_FOUND

from core.dependencies import init_model
from core.exceptions import EntityDoesNotExist
from models.api_call import ApiCallModel
from schema.api_call import ApiCallInDB, ApiCallInResponse

router = APIRouter()


@router.get("/", response_model=List[ApiCallInResponse], name="api_call:get_with_filters")
async def filter_api_calls(
        user_uuid: UUID4 = Query(None),
        style_id: int = Query(None),
        from_datetime: datetime = Query(None),
        to_datetime: datetime = Query(None),
        model: ApiCallModel = Depends(init_model(ApiCallModel))
) -> List[ApiCallInResponse]:
    api_calls = await model.get_many(
        user_uuid=user_uuid,
        style_id=style_id,
        from_datetime=from_datetime,
        to_datetime=to_datetime
    )
    return api_calls


@router.get("/{api_call_id}", response_model=ApiCallInDB, name="api_call:get_single")
async def get_api_call(
        api_call_id: int,
        model: ApiCallModel = Depends(init_model(ApiCallModel))
) -> ApiCallInDB:
    try:
        api_call = await model.get_by_id(api_call_id)
        return ApiCallInDB(**api_call.dict())
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="User with this uuid does not exist."
        )
