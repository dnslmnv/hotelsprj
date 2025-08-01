from unittest import mock
patcher = mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f)
patcher.start()

from pathlib import Path
import json

import pytest
from httpx import AsyncClient


from src.api.dependencies import get_db
from src.config import settings
from src.main import app
from src.models import *
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.schemas.rooms import RoomAdd
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager




@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="function")
async def db() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

async def get_db_null_pool():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db

app.dependency_overrides[get_db] = get_db_null_pool

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open("test/mock_hotels.json", mode="r", encoding="utf-8") as file_hotels:
        hotels = json.load(file_hotels)

    with open("test/mock_rooms.json", mode="r", encoding="utf-8") as file_rooms:
        rooms = json.load(file_rooms)

    hotels = [HotelAdd.model_validate(hotel) for hotel in hotels]
    rooms = [RoomAdd.model_validate(room) for room in rooms]
    async with DBManager(session_factory=async_session_maker_null_pool) as db_:
        await db_.hotels.add_bulk(hotels)
        await db_.rooms.add_bulk(rooms)
        await db_.commit()

@pytest.fixture(scope="session", autouse=True)
async def ac() -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session", autouse=True)
async def register_user(ac, setup_database):
    await ac.post(
    "/auth/register",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )

@pytest.fixture(scope="session", autouse=True)
async def authenticated_ac(register_user, ac):
    result = await ac.post(
    "/auth/login",
        json={
            "email": "kot@pes.com",
            "password": "1234"
        }
    )
    assert ac.cookies["access_token"]
    yield ac

