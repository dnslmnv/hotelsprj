from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {"id":1, "title":"Sochi", "name": "5star"},
    {"id":2, "title":"Дубай", "name": "Jingle"},
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="Айди отеля"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@router.delete("/{hotel_id}")
def delete_hotels(
    hotel_id: int,
):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("")
def create_hotels(
        hotel_data: Hotel = Body(openapi_examples={"1": {"summary": "Tver", "value": {"title": "Tver", "name": "Volga"}},
                                                   "2": {"summary": "Moscow", "value": {"title": "Moscow", "name": "4 Seasons"}}
                                                   })
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name" : hotel_data.name
    })
    return {"status": "OK"}


@router.put("/{hotel_id}")
def edit_hotels_put(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
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
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}