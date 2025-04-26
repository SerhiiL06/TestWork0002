from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.task_service import TaskService
from backend.presentation.common.factories import current_user
from backend.presentation.models.tasks import CreateTask, UpdateTask

tasks_router = APIRouter()


@tasks_router.get("/tasks")
async def get_tasks(): ...


@tasks_router.get("/tasks/search")
async def search_tasks(): ...


@tasks_router.get("/tasks/{task_id}")
async def get_task(task_id: int): ...


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
async def update_task(task_id: str, task: UpdateTask): ...
