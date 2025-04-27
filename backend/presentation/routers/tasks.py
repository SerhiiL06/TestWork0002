from datetime import datetime
from typing import Literal

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.task_service import TaskService
from backend.presentation.common.factories import current_user
from backend.presentation.models.filters import TaskFilter
from backend.presentation.models.tasks import CreateTask, UpdateTask

tasks_router = APIRouter(tags=["tasks"])


@tasks_router.get("/tasks")
@inject
async def get_tasks(
    user: current_user,
    session: FromDishka[AsyncSession],
    service: FromDishka[TaskService],
    status: Literal["PENDING", "DONE"] | None = None,
    priority: int | None = None,
    date_gte: datetime | None = None,
    date_lte: datetime | None = None,
):
    return await service.get_user_tasks(
        user.get("user_id"), session, TaskFilter(status, priority, date_gte, date_lte)
    )


@tasks_router.get("/tasks/search")
@inject
async def search_tasks(
    user: current_user,
    session: FromDishka[AsyncSession],
    service: FromDishka[TaskService],
    q: str = Query(required=False, default=None, description="Search by title and description"),
):
    return await service.get_user_tasks(user.get("user_id"), session, text=q)


@tasks_router.post("/tasks")
@inject
async def create_task(
    task: CreateTask,
    user: current_user,
    session: FromDishka[AsyncSession],
    service: FromDishka[TaskService],
):
    return await service.create_task(task, user.get("user_id"), session)


@tasks_router.put("/tasks/{task_id}")
@inject
async def update_task(
    task_id: int,
    task: UpdateTask,
    user: current_user,
    session: FromDishka[AsyncSession],
    service: FromDishka[TaskService],
):
    return await service.update_task(task_id, task, user.get("user_id"), session)
