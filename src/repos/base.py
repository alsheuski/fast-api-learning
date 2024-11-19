from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from helpers import print_sql


class BaseRepository:
    model = None
    schema: BaseModel = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        if self.model:
            query = select(self.model)
            result = await self.session.execute(query)

            return [
                self.schema.model_validate(model, from_attributes=True)
                for model in result.scalars().all()
            ]

    async def get_one_or_none(self, **filter_by):
        if self.model:
            query = select(self.model).filter_by(**filter_by)
            result = await self.session.execute(query)

            obj = result.scalars().one_or_none()
            if obj is not None:
                return self.schema.model_validate(obj, from_attributes=True)

    async def create(self, data: BaseModel):
        if self.model:
            add_stmt = (
                insert(self.model).values(**data.model_dump()).returning(self.model)
            )
            print_sql(add_stmt)

            res = await self.session.execute(add_stmt)
            model = res.scalars().one()

            return self.schema.model_validate(model, from_attributes=True)

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
