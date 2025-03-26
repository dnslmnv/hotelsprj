from fastapi import Query, Body, APIRouter
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from passlib.context import CryptContext


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = "24kjk34l21jkopi"
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status":"OK"}