import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_login(transport: ASGITransport, user: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(url="/register", json=user)

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": user.get("password_1")},
        )
        assert response.status_code == 200
        assert bool(response.json().get("access_token"))
        assert bool(response.json().get("refresh_token"))
        assert bool(response.json().get("token_type"))

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": "random_password"},
        )
        assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh(transport: ASGITransport, user: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(url="/register", json=user)

        response = await ac.post(
            "/login",
            data={"username": user.get("email"), "password": user.get("password_1")},
        )

        refresh_token = response.json().get("refresh_token")

        response = await ac.post("/refresh", data={"token": refresh_token})
        assert response.status_code == 200
        assert bool(response.json().get("access_token"))
        assert bool(response.json().get("refresh_token"))
        assert bool(response.json().get("token_type"))

        wrong_refresh = "my_token"
        response = await ac.post("/refresh", data={"token": wrong_refresh})
        assert response.status_code == 401
