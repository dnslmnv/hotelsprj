import json

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task
from src.services.facilities import FacilityService
router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await FacilityService(db).get_facilities()


@router.post("")
async def create_facilities(db: DBDep, facility_data: FacilityAdd):
    facility = await FacilityService(db).create_facility(facility_data)
    return {"status": "OK", "data": facility}
