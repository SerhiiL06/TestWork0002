import pytest
from httpx import ASGITransport, AsyncClient
from pytest import fixture


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


@fixture
def correct_task() -> dict:
    return {"title": "test", "description": "test", "priority": 1}



@pytest.mark.asyncio
async def test_create_task(transport: ASGITransport, auth_headers: dict, correct_task: dict) -> None:
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
        assert bool(response.json().get("detail").get("priority"))

@pytest.mark.asyncio
async def test_get_tasks(transport: ASGITransport, auth_headers: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_without_token = await ac.get(url="/tasks")
        assert response_without_token.status_code == 401

        response = await ac.get(url="/tasks", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json().get("tasks")) == 1


        response = await ac.get(url="/tasks", headers=auth_headers, params={"priority": 2})
        assert response.status_code == 200
        assert len(response.json().get("tasks")) == 0

        response = await ac.get(url="/tasks", headers=auth_headers, params={"status": "PENDING"})
        assert response.status_code == 200
        assert len(response.json().get("tasks")) == 1



@pytest.mark.asyncio
async def test_update_task(transport: ASGITransport, auth_headers: dict, correct_task: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_without_token = await ac.get(url="/tasks")
        assert response_without_token.status_code == 401

        response = await ac.get(url="/tasks", headers=auth_headers)
        task_id = response.json()["tasks"][0].get("id")
        response = await ac.put(url=f"/tasks/{task_id}", headers=auth_headers, json={"status": "DONE"})
        assert response.status_code == 200
        assert response.json().get('task').get("status") == "DONE"

        response = await ac.put(url=f"/tasks/{task_id}", headers=auth_headers, json={"status": "TEST"})
        assert response.status_code == 422

        response = await ac.put(url=f"/tasks/{task_id}", headers=auth_headers, json={"priority": "10"})
        assert response.status_code == 400


@pytest.mark.asyncio
async def test_search_task(transport: ASGITransport, auth_headers: dict, correct_task: dict) -> None:
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response_without_token = await ac.get(url="/tasks/search")
        assert response_without_token.status_code == 401


        response = await ac.get(url="/tasks/search", headers=auth_headers, params={"q": "test"})
        assert response.status_code == 200
        assert len(response.json().get("tasks")) == 1

        response = await ac.get(url="/tasks/search", headers=auth_headers, params={"q": "random"})
        assert response.status_code == 200
        assert len(response.json().get("tasks")) == 0


