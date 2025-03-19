from httpx import delete
from sqlalchemy import select, insert, update
from pydantic import BaseModel

class BaseRepository():
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: BaseModel):
        add_data_stm = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stm)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filter_by) -> None:
        edit_data_stm = update(self.model).filter_by(**filter_by).values(**data.model_dump())
        await self.session.execute(edit_data_stm)


    async def delete(self, **filter_by) -> None:
        delete_data_stm = delete()