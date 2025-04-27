from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.models.users import User


class UserRepository:
    async def get(self, email: str, session: AsyncSession) -> User | None:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().one_or_none()

    async def create(self, user: User, session: AsyncSession) -> None:
        session.add(user)

    async def exists(self, email: str, session: AsyncSession) -> int | None:
        q = select(User).where(User.email == email)
        result = await session.execute(q)
        return result.scalar_one_or_none()
