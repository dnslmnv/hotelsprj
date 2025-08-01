from sqlalchemy import select
from pydantic import EmailStr


from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import User, UserWitHashedPassword


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        res = result.scalars().one()
        return UserWitHashedPassword.model_validate(res, from_attributes=True)
