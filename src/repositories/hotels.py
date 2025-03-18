from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(self,
                      location,
                      title,
                      limit,
                      offset
    ):
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
        return result.scalars().all()
