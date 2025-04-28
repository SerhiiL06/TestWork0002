from dataclasses import asdict
from logging import getLogger

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from backend.domain.exceptions import PermissionDenied
from backend.domain.repositories.task_repo import TaskRepository
from backend.infra.database.models.tasks import Task
from backend.presentation.models.filters import TaskFilter
from backend.presentation.models.tasks import CreateTask, UpdateTask

logger = getLogger(__name__)


class TaskService:
    def __init__(self, repo: TaskRepository):
        self._repo = repo

    async def get_user_tasks(
        self,
        user_id: int,
        session: AsyncSession,
        filters: TaskFilter | None = None,
        text: str | None = None,
    ) -> dict[str, list[Task]]:
        tasks = await self._repo.get_by_owner(user_id, session, filters, text)

        return {"tasks": tasks}

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

        logger.info(f"Created task {task_instance.id}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"task_id": task_instance.id}
        )

    async def update_task(
        self, task_id: int, task: UpdateTask, user_id: int, session: AsyncSession
    ):
        task_instance = await self._repo.get(task_id, session)

        if not task_instance or task_instance.owner_id != user_id:
            raise PermissionDenied()

        errors = await self._validate_task(task)

        if errors:
            raise HTTPException(status_code=400, detail=errors)

        task_data = await self._clear_data(task)

        await self._repo.update(task_instance.id, task_data, session)

        await session.commit()

        logger.info(f"Updated task {task_instance.id}")
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
        """
        Builds a dictionary containing only fields with non-empty values.

        Converts the `task` object to a dictionary and excludes any key-value pairs
        where the value is considered "empty" (`None`, `0`, `''`).
        """
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
