from sqlalchemy import select, insert, literal_column


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

    async def create(self, fields):
        add_stmt = insert(self.model).values(**fields).returning(literal_column("*"))

        res = await self.session.execute(add_stmt)
        return res.first()
