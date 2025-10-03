from datetime import date
from src.schemas.bookings import Booking, BookingAdd
from utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user = (await db.users.get_all())[0]
    room = (await db.rooms.get_all())[0]

    assert user
    assert room

    booking_data = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2025, month=8, day=12),
        date_to=date(year=2025, month=8, day=22),
        price=100,
    )

    await db.bookings.create(booking_data)
    await db.commit()

    # get
    added_booking: Booking = (await db.bookings.get_all())[0]
    assert added_booking

    # update
    booking_for_update = BookingAdd(
        user_id=user.id,
        room_id=room.id,
        date_from=date(year=2025, month=9, day=12),
        date_to=date(year=2025, month=9, day=22),
        price=200,
    )
    await db.bookings.edit(booking_for_update, id=added_booking.id)
    await db.commit()

    updated_booking: Booking = await db.bookings.get_one_or_none(id=added_booking.id)
    assert updated_booking.price == 200
    assert updated_booking.date_from == date(year=2025, month=9, day=12)
    assert updated_booking.date_to == date(year=2025, month=9, day=22)

    # delete
    await db.bookings.delete(id=added_booking.id)
    await db.commit()

    deleted_booking = await db.bookings.get_one_or_none(id=added_booking.id)
    assert not deleted_booking
