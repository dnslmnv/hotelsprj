from src.models.facilities import Facilities
from src.repositories.mappers.base import DataMapper
from src.schemas.facilities import Facility
from src.schemas.hotels import Hotel
from src.schemas.users import User
from src.schemas.bookings import Booking
from src.schemas.rooms import Room, RoomsWithRels

from src.models.hotels import HotelsOrm
from src.models.users import UsersOrm
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


class HotelDataMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel

class BookingDataMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking

class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema =User

class RoomsDataMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room

class RoomsDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomsWithRels

class FacilityDataMapper(DataMapper):
    db_model = Facilities
    schema = Facility

