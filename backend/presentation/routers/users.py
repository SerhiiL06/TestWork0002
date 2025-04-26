from dishka import FromDishka
from dishka.integrations.fastapi import inject
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.password_service import PasswordService
from backend.domain.services.user_service import UserService
from backend.presentation.models.users import RegisterUser
from fastapi import APIRouter, Depends, Request


users_router = APIRouter(tags=["users"])


@users_router.post("/register")
@inject
async def register(
    data: RegisterUser,
    session: FromDishka[AsyncSession],
    service: FromDishka[UserService],
    password_service: FromDishka[PasswordService],
):
    return await service.register(data, password_service, session)
