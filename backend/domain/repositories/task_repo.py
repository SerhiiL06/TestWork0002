from sqlalchemy import Sequence, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.operators import ge, le

from backend.infra.database.models.tasks import Task
from backend.presentation.models.filters import TaskFilter


class TaskRepository:
    async def get(self, task_id: int, session: AsyncSession) -> Task:
        result = await session.execute(select(Task).where(Task.id == task_id))
        return result.scalars().one_or_none()

    async def get_by_owner(
        self,
        owner_id: int,
        session: AsyncSession,
        filters: TaskFilter | None = None,
        text: str | None = None,
    ) -> Sequence[Task]:
        q = select(Task).where(Task.owner_id == owner_id)

        if filters:
            if filters.status:
                q = q.where(Task.status == filters.status)

            if filters.priority:
                q = q.where(Task.priority == filters.priority)

            if filters.date_gte:
                q = q.where(ge(Task.created_at, filters.date_gte))

            if filters.date_lte:
                q = q.where(le(Task.created_at, filters.date_lte))

        if text:
            q = q.where(
                or_(
                    Task.title.icontains(text),
                    Task.description.icontains(text),
                )
            )

        result = await session.execute(q)
        return result.scalars().all()

    async def create(self, task: Task, session: AsyncSession) -> None:
        session.add(task)

    async def update(self, task_id: int, task: dict, session: AsyncSession) -> None:
        q = update(Task).where(Task.id == task_id).values(**task)
        await session.execute(q)
