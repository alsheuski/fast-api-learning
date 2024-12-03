from datetime import date
from fastapi import Body, APIRouter, Query

from schemas.facilities import RoomFacilityAdd
from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels/{hotel_id}/rooms", tags=["Rooms"])


@router.get("")
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    date_from: date = Query(example="2024-08-01"),
    date_to: date = Query(example="2024-10-01"),
):
    return await db.rooms.get_filtered_by_time(
        hotel_id=hotel_id, date_from=date_from, date_to=date_to
    )


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
                    "facilities_ids": [],
                },
            },
            "2": {
                "summary": "VIP apartment",
                "value": {
                    "title": "VIP apartments",
                    "description": "VIP level of aparmtents",
                    "price": 100,
                    "quantity": 1,
                    "facilities_ids": [],
                },
            },
        }
    ),
):
    data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.create(data=data)

    rooms_facilities_data = [
        RoomFacilityAdd(room_id=room.id, facility_id=f_id)
        for f_id in room_data.facilities_ids
    ]
    await db.rooms_facilities.create_bulk(rooms_facilities_data)
    await db.commit()

    return {
        "status": "OK",
        "data": room,
    }


@router.put("/{room_id}")
async def replace_room(
    db: DBDep, room_id: int, hotel_id: int, room_data: RoomAddRequest
):
    data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(data, id=room_id)
    await db.commit()

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
    await db.commit()

    return {"status": "OK"}


@router.delete("/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}
