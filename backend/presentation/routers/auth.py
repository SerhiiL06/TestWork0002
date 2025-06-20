from typing import Annotated

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.auth_service import AuthService

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/login")
@inject
async def login(
    session: FromDishka[AsyncSession],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: FromDishka[AuthService],
):
    return await service.login(form_data.username, form_data.password, session)


@auth_router.post("/refresh")
@inject
async def refresh(
    session: FromDishka[AsyncSession],
    service: FromDishka[AuthService],
    token: str = Form(None),
):
    return await service.refresh_token(token, session)
