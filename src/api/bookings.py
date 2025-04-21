from fastapi import APIRouter


from src.api.dependencies import DBDep
from src.schemas.bookings import BookingAddRequest

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("/")
async def add_booking(
        db: DBDep,
        data: BookingAddRequest
):
    pass