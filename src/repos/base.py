from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.repos.mappers.base import DataMapper


class BaseRepository:
    model = None
    schema: BaseModel | None = None
    mapper: DataMapper | None = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        if self.model:
            query = select(self.model).filter(*filter).filter_by(**filter_by)
            result = await self.session.execute(query)

            return [
                self.mapper.map_to_domain_entity(model)
                for model in result.scalars().all()
            ]

    async def get_all(self):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        if self.model:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)

            obj = result.scalars().one_or_none()
            if obj is not None:
                return self.mapper.map_to_domain_entity(obj)

    async def create(self, data: BaseModel):
        if self.model:
            add_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )

            res = await self.session.execute(add_stmt)
            model = res.scalars().one()

            return self.mapper.map_to_domain_entity(model)

    async def create_bulk(self, data: list[BaseModel]):
        if self.model:
            add_stmt = insert(self.model).values([item.model_dump() for item in data])
            await self.session.execute(add_stmt)

    async def edit(
        self, data: BaseModel, exclude_unset: bool = False, **filter_by
    ) -> None:
        if self.model:
            stmt = (
                update(self.model)
                .filter_by(**filter_by)
                .values(**data.model_dump(exclude_unset=exclude_unset))
            )
            await self.session.execute(stmt)

    async def delete(self, **filter_by) -> None:
        if self.model:
            stmt = delete(self.model).filter_by(**filter_by)
            await self.session.execute(stmt)
