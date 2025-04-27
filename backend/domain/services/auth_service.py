from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.password_service import PasswordService
from backend.domain.services.token_service import TokenService

bearer = OAuth2PasswordBearer(tokenUrl="/login")


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
        password_service: PasswordService,
        token: TokenService,
    ) -> None:
        self._repo = repo
        self._pwd = password_service
        self._token = token

    async def login(self, email: str, password: str, session: AsyncSession) -> dict:
        instance = await self._repo.get(email, session)

        if not instance or not self._pwd.verify_pw(password, instance.hashed_password):
            raise HTTPException(401, "wrong password or email")

        payload = {
            "user_id": instance.id,
            "email": instance.email,
        }
        access = self._token.create_access_token(payload)
        refresh = self._token.create_refresh_token(payload)

        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
        }

    async def refresh_token(
        self, token: str, token_service: TokenService, session: AsyncSession
    ) -> dict:
        user_data = token_service.get_data_from_token(token, "refresh_token")

        if not user_data:
            raise HTTPException(401, "invalid token")

        instance = await self._repo.get(user_data.get("email"), session)

        if not instance:
            raise HTTPException(401, "Invalid token")

        payload = {
            "user_id": instance.id,
            "email": instance.email,
        }
        access = self._token.create_access_token(payload)
        return {"access_token": access, "refresh_token": token, "token_type": "bearer"}

    def authenticate(self, token: Annotated[str, Depends(bearer)]):
        user_data = self._token.get_data_from_token(token)
        return user_data
