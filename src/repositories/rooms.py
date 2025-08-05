from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload, joinedload

from src.exceptions import RoomNotFoundException
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.repositories.mappers.mappers import RoomsDataMapper, RoomsDataWithRelsMapper
from src.repositories.utils import rooms_ids_for_booking


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    mapper = RoomsDataMapper

    async def get_filtered_by_time(self, hotel_id, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )
        query = (
            select(self.model)
            .options(joinedload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [
            RoomsDataWithRelsMapper.map_to_domain_entity(model)
            for model in result.unique().scalars().all()
        ]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            res = result.scalars().one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomsDataWithRelsMapper.map_to_domain_entity(res)
