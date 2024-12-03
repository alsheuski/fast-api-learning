from datetime import date
from sqlalchemy import select

from src.models.rooms import RoomsOrm
from src.repos.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel
from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel

    async def get_filtered_by_time(self, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids))

    async def get_all(self, title, location, limit, offset) -> list[Hotel]:
        query = select(self.model)

        if title:
            query = query.filter(HotelsOrm.title.icontains(title))

        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            Hotel.model_validate(hotel, from_attributes=True)
            for hotel in result.scalars().all()
        ]
