from fastapi import Body, Query, APIRouter

from src.schemas.facilities import FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Facilities"])


@router.get("")
async def get_facilities(
    db: DBDep,
):
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
