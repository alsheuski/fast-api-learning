from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repos.base import BaseRepository


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self, title, location, limit, offset):
        query = select(self.model)

        if title:
            query = query.filter(HotelsOrm.title.icontains(title))

        if location:
            query = query.filter(HotelsOrm.location.icontains(location))

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return result.scalars().all()
