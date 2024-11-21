from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/booking", tags=["Booking"])


@router.get("")
async def get_all(db: DBDep):
    return await db.bookings.get_all()


@router.post("/{room_id}")
async def book_room(db: DBDep, user_id: UserIdDep, room_id: int, room_data: BookingAddRequest):
    room = await db.rooms.get_one_or_none(id=room_id)

    if not room:
        raise HTTPException(status_code=401, detail="Room not found")

    booking = BookingAdd(price=room.price, user_id=user_id, **room_data.model_dump())
    await db.bookings.create(data=booking)
    await db.commit()

    return {"status": "OK"}
