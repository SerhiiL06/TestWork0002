from dataclasses import asdict

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from backend.domain.repositories.task_repo import TaskRepository
from backend.infra.database.models.tasks import Task
from backend.presentation.models.filters import TaskFilter
from backend.presentation.models.tasks import CreateTask, UpdateTask


class TaskService:
    def __init__(self, repo: TaskRepository):
        self._repo = repo

    async def get_user_tasks(
        self,
        user_id: int,
        session: AsyncSession,
        filters: TaskFilter | None = None,
        text: str | None = None,
    ) -> list[Task]:
        return await self._repo.get_by_owner(user_id, session, filters, text)

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
        await session.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"task_id": task_instance.id}
        )

    async def update_task(
        self, task_id: int, task: UpdateTask, user_id: int, session: AsyncSession
    ):
        task_instance = await self._repo.get(task_id, session)

        if not task_instance or task_instance.owner_id != user_id:
            raise HTTPException(status_code=404, detail="Not found")

        errors = await self._validate_task(task)

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        task_data = await self._clear_data(task)

        await self._repo.update(task_instance.id, task_data, session)

        await session.commit()
        return JSONResponse(
            content={
                "task": {
                    "id": task_instance.id,
                    "title": task_instance.title,
                    "description": task_instance.description,
                    "priority": task_instance.priority,
                    "status": task_instance.status.name,
                }
            },
            status_code=status.HTTP_200_OK,
        )

    async def _clear_data(self, task: UpdateTask) -> dict:
        data = {}

        for k, v in asdict(task).items():
            if v:
                data[k] = v

        return data

    async def _validate_task(self, task: CreateTask | UpdateTask) -> dict:
        errors = {}

        if task.title and len(task.title) > 250:
            errors["title"] = "Task title too long"

        if task.priority is not None and task.priority not in range(1, 6):
            errors["priority"] = "Task priority must be between 1 and 5"

        if task.description and len(task.description) > 2000:
            errors["description"] = "Task description too long"

        return errors
