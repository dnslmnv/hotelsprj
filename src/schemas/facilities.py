from pydantic import BaseModel

class FacilityAdd(BaseModel):
    title: str

class Facility(FacilityAdd):
    id: int


class RoomFacilityAdd(BaseModel):
    facility_id: int
    room_id: int

class RoomFacility(RoomFacilityAdd):
    id: int
