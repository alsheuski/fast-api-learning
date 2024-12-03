from datetime import date
from fastapi import Body, Query, APIRouter

from src.api.dependencies import DBDep, PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None),
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-10-01"),
):
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    limit = pagination.per_page
    offset = per_page * (page - 1)

    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
        title=title,
        location=location,
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Sochi",
                "value": {"title": "Sochi Hotel", "location": "sochi_hotel"},
            },
            "2": {
                "summary": "Dubai",
                "value": {"title": "Dubai Hotel", "location": "dubai_hotel"},
            },
        }
    ),
):
    response = await db.hotels.create(data=hotel_data)
    await db.commit()

    return {
        "status": "OK",
        "data": response,
    }


@router.put("/{hotel_id}")
async def replace_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial update of some hotel details",
    description="Method can update title or name fields of exact hotel by hotel ID",
)
async def update_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}
