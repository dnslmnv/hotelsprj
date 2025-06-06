from pydantic import BaseModel
from datetime import date
from pydantic import ConfigDict

class BookingAdd(BaseModel):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int

class BookingAddRequest(BaseModel):
    room_id: int
    date_from: date
    date_to: date
    
class Booking(BookingAdd):
    id: int
    
    model_config = ConfigDict(from_attributes=True)