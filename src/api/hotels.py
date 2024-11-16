from fastapi import Body, Query, APIRouter

from src.repos.hotels import HotelsRepository
from src.database import my_async_sessionmaker
from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelAdd, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(None, description="Hotel title"),
    location: str | None = Query(None),
):
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    limit = pagination.per_page
    offset = per_page * (page - 1)

    async with my_async_sessionmaker() as session:
        return await HotelsRepository(session).get_all(title, location, limit, offset)


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with my_async_sessionmaker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(
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
    async with my_async_sessionmaker() as session:
        response = await HotelsRepository(session).create(data=hotel_data)

        await session.commit()

        return {
            "status": "OK",
            "data": response,
        }


@router.put("/{hotel_id}")
async def replace_hotel(hotel_id: int, hotel_data: HotelAdd):
    async with my_async_sessionmaker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

        return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Partial update of some hotel details",
    description="Method can update title or name fields of exact hotel by hotel ID",
)
async def update_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with my_async_sessionmaker() as session:
        await HotelsRepository(session).edit(
            hotel_data, exclude_unset=True, id=hotel_id
        )
        await session.commit()

        return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with my_async_sessionmaker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()

        return {"status": "OK"}
