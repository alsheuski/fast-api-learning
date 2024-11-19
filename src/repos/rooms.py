from sqlalchemy import select

from src.schemas.rooms import Room
from src.models.rooms import RoomsOrm
from src.repos.base import BaseRepository


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_all(self, hotel_id, title, price, limit, offset) -> list[Room]:
        query = select(self.model).filter_by(hotel_id=hotel_id)

        if title:
            query = query.filter(self.model.title.icontains(title))

        if price:
            query = query.filter_by(price=price)

        query = query.limit(limit).offset(offset)
        result = await self.session.execute(query)

        return [
            Room.model_validate(room, from_attributes=True)
            for room in result.scalars().all()
        ]
