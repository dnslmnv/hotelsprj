from pathlib import Path

import pytest
import json
from httpx import AsyncClient
from src.main import app
from src.config import settings
from src.database import Base, engine_null_pool
from src.models import *
from src.database import async_session_maker_null_pool
from src.schemas.hotels import HotelAdd
from src.utils.db_manager import DBManager
@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"

@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        mock_file = Path("mock_hotels.json")
        if not mock_file.exists():
            pytest.fail(f"Файл {mock_file} не найден!")  # Прерываем тесты с ошибкой
        with open(mock_file, "r", encoding="utf-8") as file:
            hotels_data = json.load(file)

        async with DBManager(session_factory=async_session_maker_null_pool) as db:
            for hotel in hotels_data:
                hotel_data = HotelAdd(title=hotel["title"], location=hotel["location"])
                await db.hotels.add(hotel_data)
            await db.commit()



@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )