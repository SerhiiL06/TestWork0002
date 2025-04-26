from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.models.tasks import Task


class TaskRepository:
    async def get(self, task_id: int, session: AsyncSession) -> Task:
        result = await session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().one_or_none()

    async def create(self, task: Task, session: AsyncSession) -> None:
        session.add(task)
