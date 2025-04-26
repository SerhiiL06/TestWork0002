from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from backend.domain.repositories.task_repo import TaskRepository
from backend.infra.database.models.tasks import Task
from backend.presentation.models.tasks import CreateTask, UpdateTask


class TaskService:
    def __init__(self, repo: TaskRepository):
        self._repo = repo

    async def create_task(
        self, task: CreateTask, owner_id: int, session: AsyncSession
    ) -> JSONResponse:
        errors = await self._validate_task(task)

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        task_instance = Task(
            title=task.title,
            description=task.description,
            priority=task.priority,
            owner_id=owner_id,
        )

        await self._repo.create(task_instance, session)
        await session.flush([task_instance])
        await session.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"task_id": task_instance.id}
        )

    async def update_task(
            self, task: UpdateTask, user_id: int, session: AsyncSession
    ):


        errors = await self._validate_task(task)



    async def _validate_task(self, task: CreateTask | UpdateTask) -> dict:
        errors = {}

        if len(task.title) > 250:
            errors["title"] = "Task title too long"

        if task.priority not in range(1, 6):
            errors["priority"] = "Task priority must be between 1 and 5"

        if task.description and len(task.description) > 2000:
            errors["description"] = "Task description too long"

        return errors
