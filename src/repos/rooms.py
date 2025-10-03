from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from repos.mappers.mappers import RoomDatamapper
from src.repos.utils import rooms_ids_for_booking
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository
from src.schemas.rooms import RoomWithRels


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomDatamapper

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )

        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        return [
            RoomWithRels.model_validate(model, from_attributes=True)
            for model in result.unique().scalars().all()
        ]

    async def get_one_or_none(self, **filter_by):
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)

        obj = result.unique().scalars().one_or_none()
        if obj is not None:
            return RoomWithRels.model_validate(obj, from_attributes=True)
