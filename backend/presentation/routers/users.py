from sqlalchemy.ext.asyncio import AsyncSession

from backend.presentation.models.users import RegisterUser
from fastapi import APIRouter, Depends, Request


users_router = APIRouter(tags=["users"])


@users_router.post("/register")
async def register(data: RegisterUser, session: AsyncSession, service: ...):
    return await service.register(data, session)


@users_router.post("/login")
async def login(): ...


@users_router.get("/refresh")
async def refresh(): ...
