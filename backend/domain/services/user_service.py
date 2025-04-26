from http.client import HTTPResponse

from fastapi import HTTPException, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.password_service import PasswordService
from backend.infra.database.models.users import User
from backend.presentation.models.users import RegisterUser


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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        incorrect = password_service.validate_password(
            user_data.password_1, user_data.password_2
        )

        if incorrect:
            raise HTTPException(status_code=400, detail=incorrect)

        hashed_password = password_service.hashing(user_data.password_2)

        user_id = await self._repo.create(
            User(email=user_data.email, hashed_password=hashed_password), session
        )
        await session.commit()

        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content={"user_id": user_id}
        )
