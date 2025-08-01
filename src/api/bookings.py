from fastapi import APIRouter


from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("")
async def add_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingAddRequest,
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    hotel = await db.hotels.get_one_or_none(id=room.hotel_id)
    room_price: int = room.price
    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_users_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)
