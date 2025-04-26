from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.services.password_service import PasswordService
from backend.presentation.models.users import RegisterUser


class UserService:
    def __init__(self, repo: ...):
        self._repo = repo

    def register(
        self,
        user_data: RegisterUser,
        password_service: PasswordService,
        session: AsyncSession,
    ) -> int: ...
