from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.domain.repositories.user_repo import UserRepository
from backend.domain.services.password_service import PasswordService
from backend.domain.services.token_service import TokenService

bearer = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    def __init__(
        self,
        repo: UserRepository,
        password_service: PasswordService,
        token: TokenService,
    ) -> None:
        self._repo = repo
        self.pwd = password_service
        self.token = token

    async def login(self, email: str, password: str, session: AsyncSession) -> dict:
        instance = await self._repo.get(email, session)

        if not instance or self.pwd.verify(password, instance.hashed_password) is False:
            raise HTTPException(401, "wrong password or email")

        payload = {
            "user_id": instance.id,
            "email": instance.email,
        }
        token = self.token.create_token(payload)
        return token

    def authenticate(self, token: Annotated[str, Depends(bearer)]):
        user_data = self.token.get_token(token)
        return user_data
