from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.auth_service import AuthService

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/login", tags=["auth"])
@inject
async def login(
    session: FromDishka[AsyncSession],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[AuthService],
):
    return await service.login(form_data.username, form_data.password, session)


@auth_router.get("/refresh")
async def refresh(): ...
