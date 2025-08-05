import logging

from asyncpg import UniqueViolationError
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.exceptions import ObjectNotFoundException, ObjectAlreadyExistsException
from src.repositories.mappers.base import DataMapper
from sqlalchemy.exc import NoResultFound, IntegrityError


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by):
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs):
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return None
        return self.mapper.map_to_domain_entity(res)

    async def get_one(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        try:
            res = result.scalars().one()
        except NoResultFound:
            raise ObjectNotFoundException
        return self.mapper.map_to_domain_entity(res)

    async def add(self, data: BaseModel):
        try:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            return self.mapper.map_to_domain_entity(result.scalars().one())
        except IntegrityError as ex:
            logging.error(f"Не удалось добавить данные в БД. Входные данные: {data}. Тип ошибки: {type(ex.orig.__cause__)}")
            if isinstance(ex.orig.__cause__, UniqueViolationError):
                raise ObjectAlreadyExistsException from ex
            else:
                logging.error(f"Незнакомая ошибка. Входные данные: {data}. Тип ошибки: {type(ex.orig.__cause__)}")
                raise ex

    async def add_bulk(self, data: list[BaseModel]):
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> None:
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filter_by) -> None:
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        await self.session.execute(delete_data_stmt)
