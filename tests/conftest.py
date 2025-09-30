import json
import pytest
from httpx import ASGITransport, AsyncClient

from schemas.hotels import HotelAdd
from schemas.rooms import RoomAdd
from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool, my_async_sessionmaker_null_pool
from src.utils.db_manager import DBManager
from src.models import *


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=my_async_sessionmaker_null_pool) as db:
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with DBManager(session_factory=my_async_sessionmaker_null_pool) as db_:
        with open("tests/mock_hotels.json", encoding="UTF-8") as hotels_file:
            data = json.load(hotels_file)

            data_to_add = [HotelAdd.model_validate(item) for item in data]
            await db_.hotels.create_bulk(data_to_add)

        with open("tests/mock_rooms.json", encoding="UTF-8") as rooms_file:
            data = json.load(rooms_file)

            data_to_add = [RoomAdd.model_validate(item) for item in data]
            await db_.rooms.create_bulk(data_to_add)

        await db_.commit()


@pytest.fixture(scope="session")
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def test_register_root(ac, setup_database):
    await ac.post("/auth/register", json={"email": "test@test.com", "password": "1234"})
