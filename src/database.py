from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy import text
from src.config import settings
import asyncio

engine = create_async_engine(settings.DB_URL)


async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

#raw sql request
# async def func():
#     async with engine.begin() as conn:
#         res = await conn.execute(text("SELECT version()"))
#         print(res.fetchone())
#
# asyncio.run(func())