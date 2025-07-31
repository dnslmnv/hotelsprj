from pydantic import BaseModel
from datetime import date
from pydantic import ConfigDict


class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class BookingPatch(BaseModel):
    user_id: int | None = None
    room_id: int | None = None
    date_from: date | None = None
    date_to: date | None = None
    price: int | None = None


class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class Booking(BookingAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)
