from sqlalchemy.ext.asyncio import AsyncSession

from backend.infra.database.models.users import User


class UserRepository:
    async def create(self, user: User, session: AsyncSession) -> None:
        session.add(user)
