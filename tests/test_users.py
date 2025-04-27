import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_register(transport: ASGITransport) -> None:
    correct_user = {
        "name": "test",
        "email": "admin@gmail.com",
        "password_1": "string_1",
        "password_2": "string_1",
    }
    diff_passwords = {
        "name": "test",
        "email": "admin1@gmail.com",
        "password_1": "string_1",
        "password_2": "string_2",
    }
    short_pw = {
        "name": "test",
        "email": "admin2@gmail.com",
        "password_1": "string",
        "password_2": "string",
    }
    already_exists = correct_user

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/register", json=correct_user)
        assert response.status_code == 201
        assert bool(response.json().get("user_id"))

        response = await ac.post("/register", json=diff_passwords)
        assert response.status_code == 400
        assert bool(response.json().get("detail", {}).get("password"))

        response = await ac.post("/register", json=short_pw)
        assert response.status_code == 400
        assert bool(response.json().get("detail", {}).get("length"))

        response = await ac.post("/register", json=already_exists)
        assert response.status_code == 400
        assert response.json().get("detail", {}).get("email")
