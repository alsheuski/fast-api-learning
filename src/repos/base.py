from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from helpers import print_sql


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()

    async def create(self, data: BaseModel):
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)

        res = await self.session.execute(add_stmt)
        return res.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        stmt = update(self.model)

        for filter_key, value in filter_by.items():
            if value is not None:
                stmt = stmt.where(getattr(self.model, filter_key) == value)

        print(stmt.compile(compile_kwargs={"literal_binds": True}))

        stmt = stmt.values(**data.model_dump())
        await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        stmt = delete(self.model)

        for filter_key, value in filter_by.items():
            if value is not None:
                stmt = stmt.where(getattr(self.model, filter_key) == value)

        print_sql(stmt)
        await self.session.execute(stmt)
