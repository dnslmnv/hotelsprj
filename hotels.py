from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


hotels = [
    {
        "id": 1,
        "title": "Sochi",
        "name": "5star"
    },
    {
        "id": 2,
        "title": "Dubai",
        "name": "Jingle"
    },
    {
        "id": 3,
        "title": "Paris",
        "name": "Luxury"
    },
    {
        "id": 4,
        "title": "Tokyo",
        "name": "Premium"
    },
    {
        "id": 5,
        "title": "London",
        "name": "Elite"
    },
    {
        "id": 6,
        "title": "Beijing",
        "name": "Diamond"
    },
    {
        "id": 7,
        "title": "Moscow",
        "name": "Platinum"
    },
    {
        "id": 8,
        "title": "Sydney",
        "name": "Gold"
    },
    {
        "id": 9,
        "title": "Bangkok",
        "name": "Silver"
    },
    {
        "id": 10,
        "title": "Singapore",
        "name": "Bronze"
    },
    {
        "id": 11,
        "title": "Rome",
        "name": "Crystal"
    },
    {
        "id": 12,
        "title": "Barcelona",
        "name": "Pearl"
    },
    {
        "id": 13,
        "title": "Berlin",
        "name": "Ruby"
    },
    {
        "id": 14,
        "title": "Madrid",
        "name": "Emerald"
    },
    {
        "id": 15,
        "title": "Prague",
        "name": "Sapphire"
    },
    {
        "id": 16,
        "title": "Vienna",
        "name": "Amethyst"
    },
    {
        "id": 17,
        "title": "Athens",
        "name": "Topaz"
    },
    {
        "id": 18,
        "title": "Stockholm",
        "name": "Opal"
    },
    {
        "id": 19,
        "title": "Copenhagen",
        "name": "Turquoise"
    },
    {
        "id": 20,
        "title": "Helsinki",
        "name": "Aquamarine"
    },
    {
        "id": 21,
        "title": "Oslo",
        "name": "Peridot"
    },
    {
        "id": 22,
        "title": "Zurich",
        "name": "Garnet"
    },
    {
        "id": 23,
        "title": "Geneva",
        "name": "Onyx"
    },
    {
        "id": 24,
        "title": "Milan",
        "name": "Jade"
    },
    {
        "id": 25,
        "title": "Venice",
        "name": "Corals"
    },
    {
        "id": 26,
        "title": "Amsterdam",
        "name": "Moonstone"
    },
    {
        "id": 27,
        "title": "Dublin",
        "name": "Sunstone"
    }
]


@router.get("")
def get_hotels(
        id: int | None = Query(None, description="Айди отеля"),
        title: str | None = Query(None, description="Название отеля"),
        page: int | None = Query(None, description="Страница отображения"),
        per_page: int | None = Query(None, description="Количество элементов на странице")
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)

    counter = 0
    if page: counter += 1
    if per_page: counter += 1
    if counter < 2:
        return {"status": "ERROR"}
    if counter == 2:
        length = len(hotels_)
        end_position = (page * per_page)
        start_position = end_position - per_page
        if start_position > length - 1: return {"status": "ERROR"}
        end_position = end_position if end_position < length else length
        return hotels_[start_position: end_position]
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