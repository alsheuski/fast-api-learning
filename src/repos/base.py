from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.helpers import print_sql


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        if self.model:
            query = select(self.model)
            result = await self.session.execute(query)

            return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        if self.model:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)

            return result.scalars().one_or_none()

    async def create(self, data: BaseModel):
        if self.model:
            add_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )

            res = await self.session.execute(add_stmt)
            return res.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        if self.model:
            stmt = update(self.model).filter_by(**filter_by).values(**data.model_dump())
            await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        if self.model:
            stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt)
