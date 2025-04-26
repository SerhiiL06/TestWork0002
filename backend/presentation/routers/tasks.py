from fastapi import APIRouter

from backend.presentation.models.tasks import CreateTask, UpdateTask

tasks_router = APIRouter()


@tasks_router.get("/tasks")
async def get_tasks(): ...


@tasks_router.get("/tasks/search")
async def search_tasks(): ...


@tasks_router.get("/tasks/{task_id}")
async def get_task(task_id: int): ...


@tasks_router.post("/tasks")
async def create_task(task: CreateTask): ...


@tasks_router.put("/tasks/{task_id}")
async def update_task(task_id: str, task: UpdateTask): ...
