from fastapi import Query, Body, APIRouter
from src.schemas.hotels import Hotel, HotelPATCH
from src.api.dependencies import PaginationDep


router = APIRouter(prefix="/hotels", tags=["Отели"])


# hotels = [
#     {
#         "id": 1,
#         "title": "Sochi",
#         "name": "5star"
#     },
#     {
#         "id": 2,
#         "title": "Dubai",
#         "name": "Jingle"
#     },
#     {
#         "id": 3,
#         "title": "Paris",
#         "name": "Luxury"
#     },
#     {
#         "id": 4,
#         "title": "Tokyo",
#         "name": "Premium"
#     },
#     {
#         "id": 5,
#         "title": "London",
#         "name": "Elite"
#     },
#     {
#         "id": 6,
#         "title": "Beijing",
#         "name": "Diamond"
#     },
#     {
#         "id": 7,
#         "title": "Moscow",
#         "name": "Platinum"
#     },
#     {
#         "id": 8,
#         "title": "Sydney",
#         "name": "Gold"
#     },
#     {
#         "id": 9,
#         "title": "Bangkok",
#         "name": "Silver"
#     },
#     {
#         "id": 10,
#         "title": "Singapore",
#         "name": "Bronze"
#     },
#     {
#         "id": 11,
#         "title": "Rome",
#         "name": "Crystal"
#     },
#     {
#         "id": 12,
#         "title": "Barcelona",
#         "name": "Pearl"
#     },
#     {
#         "id": 13,
#         "title": "Berlin",
#         "name": "Ruby"
#     },
#     {
#         "id": 14,
#         "title": "Madrid",
#         "name": "Emerald"
#     },
#     {
#         "id": 15,
#         "title": "Prague",
#         "name": "Sapphire"
#     },
#     {
#         "id": 16,
#         "title": "Vienna",
#         "name": "Amethyst"
#     },
#     {
#         "id": 17,
#         "title": "Athens",
#         "name": "Topaz"
#     },
#     {
#         "id": 18,
#         "title": "Stockholm",
#         "name": "Opal"
#     },
#     {
#         "id": 19,
#         "title": "Copenhagen",
#         "name": "Turquoise"
#     },
#     {
#         "id": 20,
#         "title": "Helsinki",
#         "name": "Aquamarine"
#     },
#     {
#         "id": 21,
#         "title": "Oslo",
#         "name": "Peridot"
#     },
#     {
#         "id": 22,
#         "title": "Zurich",
#         "name": "Garnet"
#     },
#     {
#         "id": 23,
#         "title": "Geneva",
#         "name": "Onyx"
#     },
#     {
#         "id": 24,
#         "title": "Milan",
#         "name": "Jade"
#     },
#     {
#         "id": 25,
#         "title": "Venice",
#         "name": "Corals"
#     },
#     {
#         "id": 26,
#         "title": "Amsterdam",
#         "name": "Moonstone"
#     },
#     {
#         "id": 27,
#         "title": "Dublin",
#         "name": "Sunstone"
#     }
# ]


@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айди отеля"),
        title: str | None = Query(None, description="Название отеля")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    if pagination.page and pagination.per_page:
        #chain slicing
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
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