import json
from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep
from src.init import redis_manager

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
@cache(expire=20)
async def get_facilities(
    db: DBDep,
):
    print ("Go TO DB")
    return await db.facilities.get_all()


@router.post("")
async def create_facility(
    db: DBDep,
    facility_data: FacilityAdd = Body(
        openapi_examples={
            "1": {
                "summary": "TV",
                "value": {"title": "TV"},
            },
            "2": {
                "summary": "Sauna",
                "value": {"title": "Sauna"},
            },
        }
    ),
):
    response = await db.facilities.create(data=facility_data)
    await db.commit()

    return {
        "status": "OK",
        "data": response,
    }
