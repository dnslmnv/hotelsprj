from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel
    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset
    ) -> list[Hotel]:
        get_hotel_query = select(HotelsOrm)
        if location:
            get_hotel_query = (
                get_hotel_query
                .filter(func.lower(HotelsOrm.location)
                        .contains(location.strip().lower()))
            )
        if title:
            get_hotel_query = (
                get_hotel_query
                .filter(func.lower(HotelsOrm.location)
                        .contains(title.strip().lower()))
            )
        get_hotel_query = (
            get_hotel_query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(get_hotel_query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
