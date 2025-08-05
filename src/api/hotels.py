from datetime import date
from fastapi_cache.decorator import cache

from fastapi import Query, Body, APIRouter

from src.exceptions import (
    ObjectNotFoundException,
    HotelNotFoundHTTPException,
)
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

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
    hotels = await HotelService(db).get_filtered_by_time(
        pagination,
        location,
        title,
        date_from,
        date_to
    )
    return {"status": "OK", "data": hotels}


@router.get("/{hotel_id}")
async def get_hotel(
    hotel_id: int,
    db: DBDep,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except ObjectNotFoundException as ex:
        raise HotelNotFoundHTTPException


@router.delete("/{hotel_id}")
async def delete_hotels(hotel_id: int, db: DBDep):
    await HotelService(db).delete_hotel(hotel_id=hotel_id)
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
    hotel = await HotelService(db).create_hotel(hotel_data=hotel_data)
    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="обновление данных об отеле",
    description="передавать все значения",
)
async def edit_hotels_put(hotel_id: int, db: DBDep, hotel_data: HotelAdd = Body()):
    await HotelService(db).edit_hotel_put(hotel_id, hotel_data)
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных об отеле",
    description="Можно передавать не все значения",
)
async def edit_hotels_patch(hotel_id: int, db: DBDep, hotel_data: HotelPATCH):
    await HotelService(db).edit_hotel_patch(hotel_id, hotel_data)
    return {"status": "OK"}
