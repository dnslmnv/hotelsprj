import json

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
@cache(expire=10)
async def get_facilities(
    db: DBDep,
):
    return await db.facilities.get_all()


@router.post("")
async def create_facilities(db: DBDep, data: FacilityAdd):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}
