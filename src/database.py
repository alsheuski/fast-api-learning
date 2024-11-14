from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(url=settings.DB_URL)

my_async_sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
session = my_async_sessionmaker()


class Base(DeclarativeBase):
    pass
