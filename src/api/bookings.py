from fastapi import APIRouter, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingAddRequest


router = APIRouter(prefix="/booking", tags=["Booking"])


@router.get("")
async def get_all(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_bookings_me(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def book_room(
    db: DBDep, user_id: UserIdDep, booking_request_data: BookingAddRequest
):
    room = await db.rooms.get_one_or_none(id=booking_request_data.room_id)

    if not room:
        raise HTTPException(status_code=401, detail="Room not found")

    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)

    if not hotel:
        raise HTTPException(status_code=401, detail="Hotel not found")

    booking_data = BookingAdd(
        price=room.price, user_id=user_id, **booking_request_data.model_dump()
    )
    booking = await db.bookings.add_booking(data=booking_data, hotel_id=hotel.id)
    await db.commit()

    return {"status": "OK", "data": booking}
