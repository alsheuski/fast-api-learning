from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
from src.database import my_async_sessionmaker_null_pool


async def test_add_hotel():
    hotel_data = HotelAdd(title="Hotel 5 start", location="Sochi")

    async with DBManager(session_factory=my_async_sessionmaker_null_pool) as db:
        new_hotel_data = await db.hotels.create(hotel_data)
        await db.commit()
