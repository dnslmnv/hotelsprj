from fastapi import APIRouter, HTTPException, Response, Request
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta


from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.config import settings
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
        data: UserRequestAdd
):
    hashed_password = AuthService().hash_password(password=data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status":"OK"}


@router.post("/login")
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегестрирован")
        if not AuthService().verify_password(
            plain_password=data.password,
            hashed_password=user.hashed_password
            ):
            raise HTTPException(status_code=401, detail="Неверный пароль")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/me")
async def me(
    request: Request,
    user_id: UserIdDep,
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user
    
    
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}