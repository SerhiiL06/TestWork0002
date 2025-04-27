import pytest

from pytest import fixture
from httpx import AsyncClient, ASGITransport


@fixture
async def access_token(user: dict, transport: ASGITransport) -> str:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(url="/register", json=user)
        response = await ac.post(
            url="/login",
            data={"username": user["email"], "password": user["password_1"]},
        )
        return response.json().get("access_token")


@fixture
async def auth_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token.strip()}",
        "accept": "application/json",
    }


@pytest.mark.asyncio
async def test_get_tasks(transport: ASGITransport, auth_headers: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_without_token = await ac.get(url="/tasks")
        assert response_without_token.status_code == 401

        response = await ac.get(url="/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert response.json().get("tasks") == []


@pytest.mark.asyncio
async def test_create_task(transport: ASGITransport, auth_headers: dict) -> None:
    correct_task = {"title": "test", "description": "test", "priority": 1}
    invalid_task = {"title": "test", "description": "test", "priority": 0}

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_without_token = await ac.post(url="/tasks")
        assert response_without_token.status_code == 401

        response = await ac.post(
            url="/tasks",
            headers=auth_headers,
            json=correct_task,
        )

        assert response.status_code == 201
        assert response.json().get("task_id") == 1

        response = await ac.post(
            url="/tasks",
            headers=auth_headers,
            json=invalid_task,
        )

        assert response.status_code == 400
        assert bool(response.json().get("detail").get("priority")) == True
