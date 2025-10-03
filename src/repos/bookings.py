from fastapi.exceptions import HTTPException
from repos.mappers.mappers import BookingDatamapper
from repos.utils import rooms_ids_for_booking
from schemas.bookings import BookingAdd
from src.repos.base import BaseRepository
from src.models.bookings import BookingsOrm


class BookingRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDatamapper

    async def add_booking(self, data: BookingAdd, hotel_id: int):
        rooms_ids_to_get_query = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=data.date_from, date_to=data.date_to
        )

        rooms_ids_response = await self.session.execute(rooms_ids_to_get_query)
        rooms_ids = rooms_ids_response.scalars().all()

        if data.room_id in rooms_ids:
            new_booking = await self.create(data)
            return new_booking
        else:
            raise HTTPException(500)
