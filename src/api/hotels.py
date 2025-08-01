from datetime import date
from fastapi_cache.decorator import cache

from fastapi import Query, Body, APIRouter

from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository


router = APIRouter(prefix="/hotels", tags=["Отели"])

@cache(expire=10)
@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description="Адрес"),
    title: str | None = Query(None, description="Название"),
    date_from: date = Query(),
    date_to: date = Query(),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        limit=pagination.per_page or 5,
        offset=per_page * (pagination.page - 1),
    )


@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep,):
    hotel = await db.hotels.get_one_or_none(id=hotel_id)
    return hotel
@router.delete("/{hotel_id}")
async def delete_hotels(
    hotel_id: int,
    db: DBDep
):
    hotel = await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("")
async def create_hotels(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {"summary": "Tver", "value": {"title": "Volga", "location": "Tver"}},
            "2": {
                "summary": "Moscow",
                "value": {"title": "Tver", "location": "Moscow"},
            },
        }
    ),
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="обновление данных об отеле",
    description="передавать все значения",
)
async def edit_hotels_put(hotel_id: int, db: DBDep,  hotel_data: HotelAdd = Body()):
    hotel = await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Можно передавать не все значения",
)
async def edit_hotels_patch(hotel_id: int, db: DBDep,  hotel_data: HotelPATCH):
    hotel = await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
