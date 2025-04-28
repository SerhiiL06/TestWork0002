from logging import getLogger

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.exceptions import UserAlreadyExists
from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.password_service import PasswordService
from backend.infra.database.models.users import User
from backend.presentation.models.users import RegisterUser

logger = getLogger(__name__)


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    async def register(
        self,
        user_data: RegisterUser,
        password_service: PasswordService,
        session: AsyncSession,
    ) -> JSONResponse:
        exists = await self._repo.exists(user_data.email, session)

        if exists:
            raise UserAlreadyExists(user_data.email)

        incorrect = password_service.validate_password(
            user_data.password_1, user_data.password_2
        )

        if incorrect:
            logger.debug(f"Incorrect password: {incorrect}")
            raise HTTPException(status_code=400, detail=incorrect)

        hashed_password = password_service.hash_pw(user_data.password_2)

        user_instance = User(
            name=user_data.name,
            email=user_data.email,
            hashed_password=hashed_password,
        )

        await self._repo.create(user_instance, session)
        await session.commit()

        logger.info(f"Created new user {user_instance.id}")
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"user_id": user_instance.id}
        )
