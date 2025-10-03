import json
import pytest
from unittest import mock
from httpx import ASGITransport, AsyncClient, Response

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwarts: lambda f: f).start()

from src.api.dependencies import get_db
from src.config import settings
from src.database import Base, engine_null_pool, my_async_sessionmaker_null_pool
from src.main import app
from src.models import *
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool():
    async with DBManager(session_factory=my_async_sessionmaker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


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


@pytest.fixture(scope="session")
async def authenticated_ac(test_register_root, ac):
    await ac.post("auth/login", json={"email": "test@test.com", "password": "1234"})

    assert ac.cookies["access_token"]

    yield ac
