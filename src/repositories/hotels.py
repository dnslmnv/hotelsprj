from datetime import date

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import HotelDataMapper
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel

class HotelsRepository(BaseRepository):
    model = HotelsOrm
    mapper = HotelDataMapper

    # async def get_all(self,
    #                   location,
    #                   title,
    #                   limit,
    #                   offset
    # ) -> list[Hotel]:


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
            location: str,
            title: str,
            limit: int,
            offset: int,
    ) -> list[Hotel]:
        rooms_ids_to_get = rooms_ids_for_booking(date_from=date_from, date_to=date_to)

        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        get_hotel_query = select(HotelsOrm).filter(HotelsOrm.id.in_(hotels_ids_to_get))

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

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

