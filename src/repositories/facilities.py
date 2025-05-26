from datetime import date


from src.repositories.base import BaseRepository
from src.models.facilities import Facilities, RoomsFacilities
from src.schemas.facilities import Facility


class FacilitiesRepository(BaseRepository):
    model = Facilities
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilities
    schema = RoomFacility