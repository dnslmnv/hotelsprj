from fastapi import APIRouter, HTTPException, Response, Request
from passlib.context import CryptContext
import jwt
from datetime import datetime, timezone, timedelta

from src.api.dependencies import DBDep
from src.exceptions import ObjectAlreadyExistsException
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.config import settings
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep
from src.exceptions import ObjectAlreadyExistsException, IncorrectPasswordHTTPException, IncorrectPasswordException, \
    EmailNotRegisteredHTTPException, EmailNotRegisteredException, UserAlreadyExistsException, \
    UserEmailAlreadyExistsHTTPException
router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(
    data: UserRequestAdd,
    db: DBDep,
):

    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def me(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(user_id)


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
