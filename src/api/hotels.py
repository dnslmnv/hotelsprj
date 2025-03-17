from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select, func
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None = Query(None, description="Название")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        get_hotel_query = select(HotelsOrm)
        if location:
            get_hotel_query = (
                get_hotel_query
                .filter(func.lower(HotelsOrm.location)
                .like(f"%{location.lower()}%"))
            )
        if title:
            get_hotel_query = (
                get_hotel_query
                .filter(func.lower(HotelsOrm.location)
                .like(f"%{title.lower()}%"))
            )
        get_hotel_query= (
            get_hotel_query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        print(get_hotel_query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await session.execute(get_hotel_query)
        hotels = result.scalars().all()
        return hotels


@router.delete("/{hotel_id}")
def delete_hotels(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
async def create_hotels(
        hotel_data: Hotel = Body(openapi_examples={"1": {"summary": "Tver", "value": {"title": "Volga", "location": "Tver"}},
                                                   "2": {"summary": "Moscow", "value": {"title": "Tver", "location": "Moscow"}}
                                                   })
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotels_put(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["location"] = hotel_data.location
    return {"status": "OK"}


@router.patch("/{hotel_id}",
           summary="Частичное обновление данных об отеле",
           description="Можно передавать не все значения")
def edit_hotels_patch(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.location:
        hotel["location"] = hotel_data.location
    return {"status": "OK"}