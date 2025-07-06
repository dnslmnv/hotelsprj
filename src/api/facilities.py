import json

from fastapi import APIRouter, Query

from src.init import redis_manager
from src.schemas.facilities import Facility, FacilityAdd
from src.api.dependencies import DBDep

router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_facilities(
        db: DBDep,
):
    facilities_from_cache = await redis_manager.get("facilities")
    if not facilities_from_cache:
        facilities =  await db.facilities.get_all()
        facilities_schemas: list[dict] = [f.dump() for f in facilities]
        facilities_json = json.dumps(facilities_schemas)
        await redis_manager.set("facilities", facilities_json, expire=10)
        return facilities
    else:
        facilities_dict = json.loads(facilities_from_cache)
        return facilities_dict

@router.post("")
async def create_facilities(
        db: DBDep,
        data: FacilityAdd
):
    facility = await db.facilities.add(data)
    await db.commit()
    return {"status": "OK", "data": facility}