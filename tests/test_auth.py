import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from pytest import fixture
from httpx import AsyncClient, ASGITransport


@fixture
def transport(app: FastAPI) -> ASGITransport:
    return ASGITransport(app)


@fixture
def user() -> dict:
    return {
        "name": "test",
        "email": "test@gmail.com",
        "password_1": "string_1",
        "password_2": "string_1",
    }


@pytest.mark.asyncio
async def test_login(
    session: AsyncSession, transport: ASGITransport, user: dict
) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(url="/register", json=user)

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": user.get("password_1")},
        )
        assert response.status_code == 200
        assert bool(response.json().get("access_token")) == True
        assert bool(response.json().get("refresh_token")) == True
        assert bool(response.json().get("token_type")) == True

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": "random_password"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh(
    session: AsyncSession, transport: ASGITransport, user: dict
) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(url="/register", json=user)

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": user.get("password_1")},
        )

        refresh_token = response.json().get("refresh_token")

        response = await ac.post("/refresh", data={"token": refresh_token})
        assert response.status_code == 200
        assert bool(response.json().get("access_token")) == True
        assert bool(response.json().get("refresh_token")) == True
        assert bool(response.json().get("token_type")) == True

        wrong_refresh = "my_token"
        response = await ac.post("/refresh", data={"token": wrong_refresh})
        assert response.status_code == 401
