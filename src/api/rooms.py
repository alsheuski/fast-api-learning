from fastapi import Body, APIRouter

from api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{room_id}")
async def get_hotel(db: DBDep, room_id: int, hotel_id: int):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
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
    data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    response = await db.rooms.create(data=data)

    return {
        "status": "OK",
        "data": response,
    }


@router.put("/{room_id}")
async def replace_room(
    db: DBDep, room_id: int, hotel_id: int, room_data: RoomAddRequest
):
    data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(data, id=room_id)

    return {"status": "OK"}


@router.patch(
    "/{room_id}",
    summary="Partial update of some room details",
    description="Method can update title or name fields of exact room by room ID",
)
async def update_hotel(
    db: DBDep, room_id: int, hotel_id: int, room_data: RoomPatchRequest
):
    data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data, exclude_unset=True, id=room_id)

    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)

    return {"status": "OK"}
