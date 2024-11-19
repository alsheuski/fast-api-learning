from fastapi import Body, Query, APIRouter

from src.repos.rooms import RoomsRepository
from src.database import my_async_sessionmaker
from src.api.dependencies import PaginationDep
from src.schemas.rooms import Room, RoomAdd, RoomPATCH

router = APIRouter(prefix="/{hotel_id}/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    pagination: PaginationDep,
    hotel_id: int,
    price: int | None = Query(None),
    title: str | None = Query(None, description="Room title"),
):
    per_page = pagination.per_page or 5
    page = pagination.page or 1
    limit = pagination.per_page
    offset = per_page * (page - 1)

    async with my_async_sessionmaker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id, title, price, limit, offset
        )


@router.get("/{room_id}")
async def get_hotel(room_id: int):
    async with my_async_sessionmaker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("")
async def create_room(
    hotel_id: int,
    room_data: RoomAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Two bedroom apartment",
                "value": {
                    "title": "Two bedrooms",
                    "description": "large room with two bedrooms",
                    "price": 10,
                    "quantity": 10,
                },
            },
            "2": {
                "summary": "VIP apartment",
                "value": {
                    "title": "VIP apartments",
                    "description": "VIP level of aparmtents",
                    "price": 100,
                    "quantity": 1,
                },
            },
        }
    ),
):
    setattr(room_data, "hotel_id", hotel_id)
    async with my_async_sessionmaker() as session:
        response = await RoomsRepository(session).create(data=room_data)

        await session.commit()

        return {
            "status": "OK",
            "data": response,
        }


@router.put("/{room_id}")
async def replace_room(room_id: int, hotel_id: int, room_data: RoomAdd):
    async with my_async_sessionmaker() as session:
        await RoomsRepository(session).edit(room_data, id=room_id, hotel_id=hotel_id)
        await session.commit()

        return {"status": "OK"}


@router.patch(
    "/{room_id}",
    summary="Partial update of some room details",
    description="Method can update title or name fields of exact room by room ID",
)
async def update_hotel(room_id: int, room_data: RoomPATCH):
    async with my_async_sessionmaker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=room_id)
        await session.commit()

        return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_room(room_id: int):
    async with my_async_sessionmaker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()

        return {"status": "OK"}
