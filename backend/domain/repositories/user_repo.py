from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.models.users import User


class UserRepository:
    async def create(self, user: User, session: AsyncSession) -> int:
        session.add(user)
        await session.flush([user])
        return user.id

    async def exists(self, email: str, session: AsyncSession) -> int | None:
        q = select(User).where(User.email == email)
        result = await session.execute(q)
        return result.scalar_one_or_none()
