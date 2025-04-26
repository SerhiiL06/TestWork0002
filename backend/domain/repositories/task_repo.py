from sqlalchemy import select, update, Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.models.tasks import Task


class TaskRepository:
    async def get(self, task_id: int, session: AsyncSession) -> Task:
        result = await session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().one_or_none()

    async def get_by_owner(
        self, owner_id: int, session: AsyncSession
    ) -> Sequence[Task]:
        q = select(Task).where(Task.owner_id == owner_id)
        result = await session.execute(q)
        return result.scalars().all()

    async def create(self, task: Task, session: AsyncSession) -> None:
        session.add(task)

    async def update(self, task_id: int, task: dict, session: AsyncSession) -> None:
        q = update(Task).where(Task.id == task_id).values(**task)
        await session.execute(q)
