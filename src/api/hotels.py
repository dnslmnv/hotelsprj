from fastapi import Query, Body, APIRouter

from sqlalchemy import insert
from src.schemas.hotels import Hotel, HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(location=location,
                                                       title=title,
                                                       limit=pagination.per_page or 5,
                                                       offset=per_page * (pagination.page - 1))


@router.get("/{hotel_id}")
async def get_hotel(
        hotel_id: int
):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id: int,
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotels(
        hotel_data: HotelAdd = Body(openapi_examples={"1": {"summary": "Tver", "value": {"title": "Volga", "location": "Tver"}},
                                                   "2": {"summary": "Moscow", "value": {"title": "Tver", "location": "Moscow"}}
                                                   })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def edit_hotels_put(
        hotel_id: int,
        hotel_data: HotelAdd = Body(openapi_examples={"1": {"summary": "Tver", "value": {"title": "Volga", "location": "Tver"}},
                                                   "2": {"summary": "Moscow", "value": {"title": "Tver", "location": "Moscow"}}
                                                   })
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Можно передавать не все значения")
async def edit_hotels_patch(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
    return {"status": "OK"}