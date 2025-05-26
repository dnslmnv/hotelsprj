from fastapi import APIRouter, Query

from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
):
    return await db.facilities.get_all()

@router.post("")
async def create_facilities(
        db: DBDep,
        data: FacilityAdd
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}