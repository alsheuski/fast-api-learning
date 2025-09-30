from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(url=settings.DB_URL)
engine_null_pool = create_async_engine(settings.DB_URL, poolclass=NullPool)

my_async_sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)
my_async_sessionmaker_null_pool = async_sessionmaker(
    bind=engine_null_pool, expire_on_commit=False
)

session = my_async_sessionmaker()


class Base(DeclarativeBase):
    pass
