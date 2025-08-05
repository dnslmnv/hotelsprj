from fastapi import HTTPException
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta

from src.config import settings
from src.services.base import BaseService
from src.exceptions import IncorrectTokenException, EmailNotRegisteredException, IncorrectPasswordException, \
    ObjectAlreadyExistsException, UserAlreadyExistsException
from src.schemas.users import UserRequestAdd, UserAdd

class AuthService(BaseService):
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
        except jwt.exceptions.DecodeError:
            raise IncorrectTokenException

    async def register_user(self, data: UserRequestAdd):
        hashed_password = self.hash_password(data.password)
        new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
        try:
            await self.db.users.add(new_user_data)
            await self.db.commit()
        except ObjectAlreadyExistsException as ex:
            raise UserAlreadyExistsException from ex

    async def login_user(self, data: UserRequestAdd) -> str:
        user = await self.db.users.get_user_with_hashed_password(email=data.email)
        if not user:
            raise EmailNotRegisteredException
        if not self.verify_password(data.password, user.hashed_password):
            raise IncorrectPasswordException
        access_token = self.create_access_token({"user_id": user.id})
        return access_token

    async def get_one_or_none_user(self, user_id: int):
        return await self.db.users.get_one_or_none(id=user_id)
